import datetime
from threading import Thread
import cv2
import numpy as np
import time

from app.db.session import SessionLocal
from app.repositories.access_log_repository import AccessLogRepository
from app.repositories.face_repository import FaceRepository
from app.services.insightface_service import InsightfaceService
from app.utils.draw import draw_korean_text_bgr
from app.utils.files import capture_image

class CameraService:
    def __init__(self, insightface_service):
        self.running = False
        self.thread = None
        self.frame = None

        self.processed_buffer = None
        self.insightface_service = insightface_service
        self.last_capture_time = time.time()

    def start(self):
        self.running = True
        self.thread = Thread(target=self.loop2, args=(), daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def read(self) -> np.ndarray:
        return self.frame

    def loop(self):
        rtsp_url = "rtsp://192.168.0.11:554/profile3/media.smp"
        cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue
            self.frame = frame

        cap.release()

    def loop2(self):
        # 1. 스레드 전용 DB 세션 생성
        db = SessionLocal()
        face_repository = FaceRepository(db)
        access_log_repository = AccessLogRepository(db)

        # 분석을 위한 얼굴 리스트 (필요 시 주기적으로 갱신 로직 추가 가능)
        list_faces = face_repository.list_faces()

        rtsp_url = "rtsp://192.168.0.11:554/profile3/media.smp"
        cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

        capture_interval = 10

        while self.running:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            # --- AI 분석 로직 시작 ---
            detected_faces = self.insightface_service.detect(frame)
            result_frame = frame.copy()
            current_frame_face_ids = []

            for detected_face in detected_faces:
                box = detected_face.bbox.astype(np.int32)
                x1, y1, x2, y2 = map(int, box)

                # 얼굴 분석
                analyzed_face = self.insightface_service.analyze(detected_face, list_faces)

                if analyzed_face:
                    current_frame_face_ids.append(analyzed_face.id)
                    color, name = (0, 255, 0), analyzed_face.name
                else:
                    current_frame_face_ids.append(None)
                    color, name = (0, 0, 255), "신원 미상"

                cv2.rectangle(result_frame, (x1, y1), (x2, y2), color, 2)
                result_frame = draw_korean_text_bgr(result_frame, str(name), (x2 + 10, max(0, y1)), 50, color)

            # --- 이미지 인코딩 ---
            ok, buffer = cv2.imencode(".jpg", result_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if ok:
                self.processed_buffer = buffer.tobytes()  # 👈 최종 결과물을 바이트로 저장

            # --- 사진 저장 로직 ---
            current_time = time.time()
            if len(detected_faces) > 0 and (current_time - self.last_capture_time > capture_interval):
                saved_image_path = capture_image(buffer)
                for f_id in current_frame_face_ids:
                    access_log_repository.save(f_id, str(saved_image_path))

                self.last_capture_time = current_time
                print(f"📸 {datetime.datetime.now()} 로그 저장 완료")

        db.close()  # 스레드 종료 시 세션 닫기
        cap.release()

    def generate_image(self, insightface_service: InsightfaceService, db):
        target_fps = 10
        interval = 1.0 / target_fps
        capture_interval = 10

        face_repository = FaceRepository(db)
        list_faces = face_repository.list_faces()
        access_log_repository = AccessLogRepository(db)

        while True:
            t0 = time.time()
            frame = self.read()
            if frame is None:
                time.sleep(0.05)
                continue

            detected_faces = insightface_service.detect(frame)
            result_frame = frame.copy()

            # 현재 프레임에서 식별된 ID들을 담을 리스트
            current_frame_face_ids = []

            for detected_face in detected_faces:
                box = detected_face.bbox.astype(np.int32)
                x1, y1, x2, y2 = map(int, box)

                analyzed_face = insightface_service.analyze(detected_face, list_faces)

                if analyzed_face is not None:
                    current_frame_face_ids.append(analyzed_face.id)
                    color = (0, 255, 0)  # Green
                    name = analyzed_face.name
                else:
                    current_frame_face_ids.append(None)
                    color = (0, 0, 255)  # Red
                    name = "신원 미상"

                cv2.rectangle(result_frame, (x1, y1), (x2, y2), color, 2)
                result_frame = draw_korean_text_bgr(bgr=result_frame, text=str(name), org=(x2 + 10, max(0, y1)),
                                                    font_size=50, color_bgr=color)

            ok, buffer = cv2.imencode(".jpg", result_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if not ok: continue

            # --- 저장 로직 개선 ---
            current_time = time.time()
            if len(detected_faces) > 0 and (current_time - self.last_capture_time > capture_interval):
                saved_image_path = capture_image(buffer)

                # 감지된 모든 얼굴에 대해 로그를 남김
                for f_id in current_frame_face_ids:
                    access_log_repository.save(f_id, str(saved_image_path))

                self.last_capture_time = current_time
                print(f"📸 {datetime.datetime.now()} {len(current_frame_face_ids)}명의 로그 저장 완료!")

            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"

            # FPS 제한
            dt = time.time() - t0
            sleep_time = interval - dt
            if sleep_time > 0:
                time.sleep(sleep_time)