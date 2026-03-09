import datetime
import logging
import os
import queue
import subprocess
import threading
import time
from dataclasses import dataclass
from typing import Optional

import cv2
import numpy as np

from app.db.session import SessionLocal
from app.repositories.access_log_repository import AccessLogRepository
from app.repositories.face_repository import FaceRepository
from app.utils.draw import draw_korean_text_bgr
from app.utils.files import capture_image

logger = logging.getLogger(__name__)


@dataclass
class FaceOverlay:
    box: tuple[int, int, int, int]
    color: tuple[int, int, int]
    name: str
    face_id: Optional[int]


class CameraProcess:
    def __init__(self, cam_id, rtsp_url, insightface_service):
        self.cam_id = cam_id
        self.rtsp_url = rtsp_url
        self.insightface_service = insightface_service

        self.width = 1280
        self.height = 720
        self.fps = 30

        # 튜닝 포인트
        self.detect_interval = 0.25       # 얼굴 탐지 주기 (초) / 4fps 정도
        self.db_refresh_interval = 300.0  # 5분마다 얼굴 캐시 갱신
        self.log_interval = 10.0          # 10초 간격 로그 저장
        self.hls_time = 1                 # HLS 세그먼트 1초
        self.hls_list_size = 3            # 플레이리스트 길이 축소
        self.ffmpeg = r"C:\sdinfo\ffmpeg\bin\ffmpeg.exe"

        self.stop_event = threading.Event()

        # 최신 프레임 공유용
        self.frame_cond = threading.Condition()
        self.latest_frame: Optional[np.ndarray] = None
        self.latest_frame_seq = 0

        # 마지막 얼굴 인식 결과 공유용
        self.overlay_lock = threading.Lock()
        self.latest_overlays: list[FaceOverlay] = []

        # 로그 저장 큐
        self.log_queue: queue.Queue[tuple[np.ndarray, list[int]]] = queue.Queue(maxsize=8)

        self.threads: list[threading.Thread] = []
        self.ffmpeg_proc: Optional[subprocess.Popen] = None

        self.known_faces = []
        self.last_db_refresh = 0.0
        self.last_log_at = 0.0

    def _get_ffmpeg_command(self):
        out_dir = os.path.join("static", "hls_output", str(self.cam_id))
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "index.m3u8")

        return [
            self.ffmpeg,
            "-hide_banner",
            "-loglevel", "error",
            "-y",

            "-f", "rawvideo",
            "-pix_fmt", "bgr24",
            "-s", f"{self.width}x{self.height}",
            "-r", str(self.fps),
            "-i", "-",

            "-an",  # rawvideo라 오디오 없음
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-tune", "zerolatency",
            "-pix_fmt", "yuv420p",
            "-profile:v", "baseline",
            "-level", "3.1",

            # HLS 세그먼트 경계 안정화
            "-g", str(self.fps),
            "-keyint_min", str(self.fps),
            "-sc_threshold", "0",

            "-f", "hls",
            "-hls_time", str(self.hls_time),
            "-hls_list_size", str(self.hls_list_size),
            "-hls_flags", "delete_segments+append_list+independent_segments+omit_endlist",
            out_path,
        ]

    def _start_ffmpeg(self):
        self._stop_ffmpeg()
        logger.info("[%s] starting ffmpeg", self.cam_id)

        self.ffmpeg_proc = subprocess.Popen(
            self._get_ffmpeg_command(),
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            bufsize=0,
        )

    def _stop_ffmpeg(self):
        proc = self.ffmpeg_proc
        self.ffmpeg_proc = None
        if proc is None:
            return

        try:
            if proc.stdin:
                proc.stdin.close()
        except Exception:
            pass

        try:
            proc.terminate()
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            proc.kill()
        except Exception:
            pass

    def _write_frame_to_ffmpeg(self, frame: np.ndarray) -> bool:
        proc = self.ffmpeg_proc
        if proc is None or proc.stdin is None:
            return False

        try:
            proc.stdin.write(frame.tobytes())
            return True
        except Exception as exc:
            logger.warning("[%s] ffmpeg pipe write failed: %s", self.cam_id, exc)
            return False

    def _refresh_known_faces(self):
        db = SessionLocal()
        try:
            face_repo = FaceRepository(db)
            self.known_faces = face_repo.list_faces()
            self.last_db_refresh = time.monotonic()
            logger.info("[%s] face cache refreshed (%d)", self.cam_id, len(self.known_faces))
        except Exception:
            logger.exception("[%s] failed to refresh face cache", self.cam_id)
        finally:
            db.close()

    def _enqueue_log(self, frame: np.ndarray, face_ids: list[Optional[int]]):
        recognized_ids = sorted({int(face_id) for face_id in face_ids if face_id})
        if not recognized_ids:
            return

        try:
            self.log_queue.put_nowait((frame, recognized_ids))
        except queue.Full:
            logger.warning("[%s] log queue full; dropping log task", self.cam_id)

    def _log_worker_loop(self):
        while not self.stop_event.is_set() or not self.log_queue.empty():
            try:
                frame, face_ids = self.log_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            db = SessionLocal()
            try:
                ok, buffer = cv2.imencode(
                    ".jpg",
                    frame,
                    [int(cv2.IMWRITE_JPEG_QUALITY), 70]
                )
                if not ok:
                    logger.warning("[%s] jpeg encode failed", self.cam_id)
                    continue

                saved_image_path = capture_image(buffer)
                access_log_repo = AccessLogRepository(db)

                for face_id in face_ids:
                    access_log_repo.save(face_id, str(saved_image_path))

                db.commit()
                logger.info("[%s] access log saved at %s", self.cam_id, datetime.datetime.now())

            except Exception:
                db.rollback()
                logger.exception("[%s] failed to save access log", self.cam_id)
            finally:
                db.close()
                self.log_queue.task_done()

    def _publish_frame(self, frame: np.ndarray):
        with self.frame_cond:
            self.latest_frame = frame
            self.latest_frame_seq += 1
            self.frame_cond.notify_all()

    def _get_latest_frame(self, last_seq: int = -1, timeout: float = 0.5):
        with self.frame_cond:
            if self.latest_frame is None:
                self.frame_cond.wait(timeout=timeout)
            elif self.latest_frame_seq == last_seq:
                self.frame_cond.wait(timeout=timeout)

            if self.latest_frame is None:
                return None, last_seq

            return self.latest_frame.copy(), self.latest_frame_seq

    def _capture_loop(self):
        backoff = 1.0

        while not self.stop_event.is_set():
            cap = None
            try:
                cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

                if not cap.isOpened():
                    raise RuntimeError("failed to open RTSP stream")

                logger.info("[%s] RTSP connected", self.cam_id)
                backoff = 1.0

                while not self.stop_event.is_set():
                    ret, frame = cap.read()
                    if not ret or frame is None:
                        raise RuntimeError("failed to read frame")

                    self._publish_frame(frame)

            except Exception as exc:
                logger.warning("[%s] capture error: %s", self.cam_id, exc)
                time.sleep(backoff)
                backoff = min(backoff * 2, 10.0)

            finally:
                if cap is not None:
                    cap.release()

    def _detect_and_recognize(self, frame: np.ndarray):
        overlays: list[FaceOverlay] = []
        face_ids: list[Optional[int]] = []

        try:
            detected_faces = self.insightface_service.detect(frame) or []
        except Exception:
            logger.exception("[%s] face detect failed", self.cam_id)
            return overlays, face_ids

        h, w = frame.shape[:2]

        for detected_face in detected_faces:
            try:
                x1, y1, x2, y2 = detected_face.bbox.astype(np.int32).tolist()
                x1 = max(0, min(x1, w - 1))
                y1 = max(0, min(y1, h - 1))
                x2 = max(0, min(x2, w - 1))
                y2 = max(0, min(y2, h - 1))

                analyzed_face = self.insightface_service.analyze(
                    detected_face,
                    self.known_faces
                )

                if analyzed_face:
                    face_id = analyzed_face.id
                    name = analyzed_face.name
                    color = (0, 255, 0)
                else:
                    face_id = None
                    name = "신원 미상"
                    color = (0, 0, 255)

                overlays.append(
                    FaceOverlay(
                        box=(x1, y1, x2, y2),
                        color=color,
                        name=name,
                        face_id=face_id,
                    )
                )
                face_ids.append(face_id)

            except Exception:
                logger.exception("[%s] face analyze failed", self.cam_id)

        return overlays, face_ids

    def _render_frame(self, frame: np.ndarray, overlays: list[FaceOverlay]) -> np.ndarray:
        for item in overlays:
            x1, y1, x2, y2 = item.box
            cv2.rectangle(frame, (x1, y1), (x2, y2), item.color, 2)
            frame = draw_korean_text_bgr(bgr=frame, text=str(item.name), org=(x2, max(20, y1 - 10)), font_size=40, color_bgr=item.color)
            # cv2.putText(
            #     frame,
            #     item.name,
            #     (x1, max(20, y1 - 10)),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     0.6,
            #     item.color,
            #     2,
            # )
        return frame

    def _inference_loop(self):
        self._refresh_known_faces()
        last_seq = -1
        last_detect_at = 0.0

        while not self.stop_event.is_set():
            frame, last_seq = self._get_latest_frame(last_seq, timeout=0.5)
            if frame is None:
                continue

            now = time.monotonic()

            if now - self.last_db_refresh >= self.db_refresh_interval:
                self._refresh_known_faces()

            if now - last_detect_at < self.detect_interval:
                continue

            overlays, face_ids = self._detect_and_recognize(frame)

            with self.overlay_lock:
                self.latest_overlays = overlays

            if overlays and (now - self.last_log_at >= self.log_interval):
                rendered = self._render_frame(frame.copy(), overlays)
                self._enqueue_log(rendered, face_ids)
                self.last_log_at = now

            last_detect_at = now

    def _stream_loop(self):
        self._start_ffmpeg()

        frame_interval = 1.0 / self.fps
        next_tick = time.monotonic()

        while not self.stop_event.is_set():
            frame, _ = self._get_latest_frame(timeout=0.5)
            if frame is None:
                continue

            with self.overlay_lock:
                overlays = list(self.latest_overlays)

            rendered = self._render_frame(frame, overlays)

            output_frame = cv2.resize(
                rendered,
                (self.width, self.height),
                interpolation=cv2.INTER_LINEAR
            )
            output_frame = np.ascontiguousarray(output_frame)

            if not self._write_frame_to_ffmpeg(output_frame):
                self._start_ffmpeg()
                continue

            next_tick += frame_interval
            sleep_for = next_tick - time.monotonic()
            if sleep_for > 0:
                time.sleep(sleep_for)
            else:
                next_tick = time.monotonic()

        self._stop_ffmpeg()

    def run(self):
        self.threads = [
            threading.Thread(target=self._capture_loop, name=f"cam-{self.cam_id}-capture", daemon=True),
            threading.Thread(target=self._inference_loop, name=f"cam-{self.cam_id}-inference", daemon=True),
            threading.Thread(target=self._stream_loop, name=f"cam-{self.cam_id}-stream", daemon=True),
            threading.Thread(target=self._log_worker_loop, name=f"cam-{self.cam_id}-log", daemon=True),
        ]

        for thread in self.threads:
            thread.start()

        try:
            while not self.stop_event.is_set():
                time.sleep(1)
        finally:
            self.stop()

    def stop(self):
        self.stop_event.set()

        with self.frame_cond:
            self.frame_cond.notify_all()

        current = threading.current_thread()
        for thread in self.threads:
            if thread is not current and thread.is_alive():
                thread.join(timeout=2)

        self._stop_ffmpeg()