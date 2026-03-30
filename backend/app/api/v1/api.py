from fastapi import APIRouter
from app.api.v1.camera import camera_router
from app.api.v1.face import face_router
from app.api.v1.snapshot import snapshot_router
from app.api.v1.stream import webrtc_router

api_router = APIRouter()

api_router.include_router(face_router.router, prefix="/faces", tags=["faces"])
api_router.include_router(camera_router.router, prefix="/cameras", tags=["cameras"])
api_router.include_router(snapshot_router.router, prefix="/snapshots", tags=["snapshots"])
api_router.include_router(webrtc_router.router, prefix='/webrtc', tags=['webrtc'])