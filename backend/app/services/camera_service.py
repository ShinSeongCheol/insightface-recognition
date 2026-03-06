import datetime
import queue
from threading import Thread, Event
import cv2
import numpy as np
import time

from app.db.session import SessionLocal
from app.repositories.access_log_repository import AccessLogRepository
from app.repositories.face_repository import FaceRepository
from app.utils.draw import draw_korean_text_bgr
from app.utils.files import capture_image


class CameraService:
    def __init__(self, insightface_service):
        self.running = False
        self.insightface_service = insightface_service

        self.frame_queue = queue.Queue(maxsize=1)
        self.processed_buffer = None
        self.new_frame_event = Event()
        self.last_capture_time = time.time()

        self.rtsp_url = "rtsp://192.168.0.11:554/profile3/media.smp"

    def _capture_thread(self):
        cap = cv2.VideoCapture(self.rtsp_url, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                time.sleep(1)  # 연결 실패 시 잠시 대기
                cap.open(self.rtsp_url)
                continue

            # 큐를 항상 최신 상태로 유지 (이전 프레임은 버림)
            if self.frame_queue.full():
                try:
                    self.frame_queue.get_nowait()
                except queue.Empty:
                    pass
            self.frame_queue.put(frame)

        cap.release()

    def _process_thread(self):
        db = SessionLocal()
        face_repo = FaceRepository(db)
        access_log_repo = AccessLogRepository(db)
        list_faces = face_repo.list_faces()

        capture_interval = 10

        while self.running:
            try:
                # 큐에서 프레임을 가져옴 (0.5초 동안 없으면 다시 시도)
                frame = self.frame_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            # 1. AI 분석 속도 향상을 위해 리사이징 (0.5배)
            scale = 0.5
            small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
            detected_faces = self.insightface_service.detect(small_frame)

            result_frame = frame.copy()
            current_frame_face_ids = []

            for detected_face in detected_faces:
                # 💡 [핵심] 0.5배에서 찾은 좌표를 원본(2배)으로 복원
                # 원본 좌표 = $작은 좌표 \times \frac{1}{scale}$
                box = (detected_face.bbox / scale).astype(np.int32)
                x1, y1, x2, y2 = map(int, box)

                analyzed_face = self.insightface_service.analyze(detected_face, list_faces)

                if analyzed_face:
                    current_frame_face_ids.append(analyzed_face.id)
                    color, name = (0, 255, 0), analyzed_face.name
                else:
                    current_frame_face_ids.append(None)
                    color, name = (0, 0, 255), "신원 미상"

                cv2.rectangle(result_frame, (x1, y1), (x2, y2), color, 2)
                result_frame = draw_korean_text_bgr(result_frame, str(name), (x1, max(0, y1 - 40)), 40, color)

            # 2. 인코딩 대상 설정 (원본 frame이 아니라 그림이 그려진 result_frame을 인코딩)
            ok, buffer = cv2.imencode(".jpg", result_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            if ok:
                self.processed_buffer = buffer.tobytes()
                self.new_frame_event.set()

            # 3. 저장 로직
            current_time = time.time()
            if len(detected_faces) > 0 and (current_time - self.last_capture_time > capture_interval):
                saved_image_path = capture_image(buffer)
                for f_id in current_frame_face_ids:
                    access_log_repo.save(f_id, str(saved_image_path))
                self.last_capture_time = current_time
                print(f"📸 {datetime.datetime.now()} 로그 저장 완료")

        db.close()

    def start(self):
        if self.running: return
        self.running = True
        Thread(target=self._capture_thread, daemon=True).start()
        Thread(target=self._process_thread, daemon=True).start()

    def stop(self):
        self.running = False

    def stream(self):
        while True:
            # 새로운 프레임 신호 대기 (타임아웃 1초)
            if not self.new_frame_event.wait(timeout=1.0):
                continue

            if self.processed_buffer:
                yield (
                        b"--frame\r\n"
                        b"Content-Type: image/jpeg\r\n\r\n" + self.processed_buffer + b"\r\n"
                )

            self.new_frame_event.clear()