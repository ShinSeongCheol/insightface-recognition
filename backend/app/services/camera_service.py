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
        last_capture_time = time.time()

        analyzed_face = None

        # 등록된 얼굴 조회
        face_repository = FaceRepository(db)
        list_faces = face_repository.list_faces()

        access_log_repository = AccessLogRepository(db)

        while True:
            t0 = time.time()

            frame: np.ndarray = self.read()
            if frame is None:
                time.sleep(0.05)
                continue

            detected_faces = insightface_service.detect(frame)  # 리스트라고 가정
            result_frame = frame.copy()

            # 박스 경계 표시
            for detected_face in detected_faces:
                box = detected_face.bbox.astype(np.int32)
                x1, y1, x2, y2 = map(int, box)

                # 얼굴 분석
                analyzed_face = insightface_service.analyze(detected_face, list_faces)

                tx, ty = x2 + 10, max(0, y1)
                if analyzed_face is not None:
                    best_name = analyzed_face.name
                    cv2.rectangle(result_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    result_frame = draw_korean_text_bgr(bgr=result_frame, text=str(best_name), org=(tx, ty), font_size=50, color_bgr=(0,255,0))
                else:
                    best_name = "신원 미상"
                    cv2.rectangle(result_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    result_frame = draw_korean_text_bgr(bgr=result_frame, text=str(best_name), org=(tx, ty), font_size=50, color_bgr=(0,0,255))


            ok, buffer = cv2.imencode(".jpg", result_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

            if not ok:
                time.sleep(0.05)
                continue

            # 사진 저장
            if len(detected_faces) > 0:
                current_time = time.time()
                elapsed_time = current_time - last_capture_time

                if elapsed_time > capture_interval:
                    saved_image_path = capture_image(buffer)

                    face_id = analyzed_face.id if analyzed_face else None
                    access_log_repository.save(face_id, str(saved_image_path))

                    last_capture_time = current_time
                    print(f"📸 {datetime.datetime.now()} 사진이 저장되었습니다! (간격: {capture_interval}초)")

            yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )

            # FPS 제한
            dt = time.time() - t0
            sleep_time = interval - dt
            if sleep_time > 0:
                time.sleep(sleep_time)