from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from sqlalchemy import select
from app.models.face import Face
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import time

router = APIRouter()
@router.get("/")
async def read(request: Request):
    camera_service = request.app.state.camera_service
    frame: np.ndarray = camera_service.read()

    _, buffer = cv2.imencode('.jpg', frame)

    return Response(content=buffer.tobytes(), media_type="image/jpeg")

@router.get("/stream")
async def read_stream(request: Request, db: Session = Depends(get_db)):
    stmt = select(Face)
    stored_faces = db.execute(stmt).scalars().all()

    camera_service = request.app.state.camera_service
    face_service = request.app.state.face_service

    def gen():
        target_fps = 10
        interval = 1.0 / target_fps

        while True:
            t0 = time.time()

            frame: np.ndarray = camera_service.read()
            if frame is None:
                time.sleep(0.05)
                continue

            detected_faces = face_service.detect(frame)  # 리스트라고 가정
            result_frame = frame.copy()

            for detected_face in detected_faces:
                box = detected_face.bbox.astype(np.int32)
                x1, y1, x2, y2 = map(int, box)


                analyzed_face = face_service.analyze(detected_face, stored_faces)

                tx, ty = x2 + 10, max(0, y1)
                if analyzed_face is not None:
                    best_name = analyzed_face.name
                    cv2.rectangle(result_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    result_frame = camera_service.draw_korean_text_bgr(bgr=result_frame, text=str(best_name), org=(tx, ty), font_size=50, color_bgr=(0,255,0))
                else:
                    best_name = "신원 미상"
                    cv2.rectangle(result_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    result_frame = camera_service.draw_korean_text_bgr(bgr=result_frame, text=str(best_name), org=(tx, ty), font_size=50, color_bgr=(0,0,255))

            ok, buffer = cv2.imencode(".jpg", result_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if not ok:
                time.sleep(0.05)
                continue

            yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n"
            )

            # FPS 제한
            dt = time.time() - t0
            sleep_time = interval - dt
            if sleep_time > 0:
                time.sleep(sleep_time)

    return StreamingResponse(
        gen(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )