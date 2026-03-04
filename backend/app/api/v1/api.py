from fastapi import APIRouter
from app.api.v1.endpoints import cameras
from app.api.v1.endpoints import faces

api_router = APIRouter()

api_router.include_router(faces.router, prefix="/faces", tags=["faces"])
api_router.include_router(cameras.router, prefix="/cameras", tags=["cameras"])