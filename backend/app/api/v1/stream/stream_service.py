from typing import List

from app.api.v1.camera import camera_repository
from app.api.v1.camera.camera_model import CameraModel
from app.api.v1.camera.camera_repository import CameraRepository


class StreamService:
    def __init__(self, insightface_service, session_factory):
        self.insightface_service = insightface_service
        self.session_factory=session_factory

    async def init(self):
        async with self.session_factory() as db:
            camera_repository = CameraRepository(db)
            camera_list: List[CameraModel] = await camera_repository.list_cameras()

            for camera in camera_list:
                print(camera.uuid)
