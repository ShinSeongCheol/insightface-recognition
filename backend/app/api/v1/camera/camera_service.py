import httpx

from app.api.v1.camera.camera_model import CameraModel
from app.api.v1.camera.camera_repository import CameraRepository
from app.api.v1.camera.camera_schema import CameraRequest
from app.api.v1.mediaMtx.mediaMtx_model import MediaMtxModel
from app.api.v1.mediaMtx.mediaMtx_repository import MediaMtxRepository
from app.api.v1.stream.stream_repository import StreamRepository


class CameraService:
    def __init__(self, db):
        self.db = db
        self.camera_repository = CameraRepository(db)
        self.media_mtx_repository = MediaMtxRepository(db)
        self.stream_repository = StreamRepository(db)

    async def list_camera(self):
        cameras = await self.camera_repository.list_cameras()
        return cameras

    async def select_camera(self, id):
        camera = await self.camera_repository.select_camera(id)
        return camera

    async def insert_camera(self, camera_data: CameraRequest) -> CameraModel:
        camera = await self.camera_repository.insert_camera(camera_data)
        return camera

    def update_camera(self, id, name, model, location, rtsp, is_active):
        camera = self.camera_repository.update_camera(id, name, model, location, rtsp, is_active)
        return camera