from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import StreamingResponse
import numpy as np
import cv2
from sqlalchemy.orm import Session

from app.db.session import async_get_db

router = APIRouter()
@router.get("/")
async def read(request: Request):
    camera_service = request.app.state.camera_service
    frame: np.ndarray = camera_service.read()

    _, buffer = cv2.imencode('.jpg', frame)

    return Response(content=buffer.tobytes(), media_type="image/jpeg")

@router.get("/stream")
async def read_stream(request: Request, db:Session = Depends(async_get_db)):
    camera_service = request.app.state.camera_service
    insightface_service = request.app.state.insightface_service

    return StreamingResponse(
        camera_service.stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )