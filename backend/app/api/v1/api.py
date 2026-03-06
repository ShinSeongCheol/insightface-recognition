from fastapi import APIRouter
from app.api.v1.endpoints import cameras
from app.api.v1.endpoints import faces
from app.api.v1.endpoints import snapshots

api_router = APIRouter()

api_router.include_router(faces.router, prefix="/faces", tags=["faces"])
api_router.include_router(cameras.router, prefix="/cameras", tags=["cameras"])
api_router.include_router(snapshots.router, prefix="/snapshots", tags=["snapshots"])