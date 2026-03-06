import datetime
from threading import Thread
import cv2
import numpy as np
import time

from app.repositories.access_log_repository import AccessLogRepository
from app.repositories.face_repository import FaceRepository
from app.services.insightface_service import InsightfaceService
from app.utils.draw import draw_korean_text_bgr
from app.utils.files import capture_image

class CameraService:
    def __init__(self):
        self.running = False
        self.thread = None
        self.frame = None

        self.last_capture_time = time.time()

    def start(self):
        self.running = True
        self.thread = Thread(target=self.loop, args=(), daemon=True)
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