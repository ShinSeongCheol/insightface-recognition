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
        media_mtx: MediaMtxModel = await self.media_mtx_repository.getMediaMtx(1)

        async with httpx.AsyncClient() as client:
            payload = {
                "name": "original/" +  str(camera_data.uuid),
                "source": camera.rtsp_url,
                "sourceOnDemand": True
            }

            response = await client.post(
                f"http://{media_mtx.ip}:{media_mtx.api_port}/v3/config/paths/add/original/{str(camera.uuid)}",
                json=payload,
                auth=("admin", "password")
            )

            if response.status_code == 200:
                print('mediaMTX 등록 성공')
                await self.stream_repository.insertStream(media_mtx_id=media_mtx.id, camera_id=camera.id, path_name="ORIGINAL")

            else:
                print(f'mediaMTX 등록 실패: {response.status_code} - {response.text}')

            payload = {
                "name": "analysis/" +  str(camera_data.uuid),
                "source": "publisher",
            }

            response = await client.post(
                f"http://{media_mtx.ip}:{media_mtx.api_port}/v3/config/paths/add/analysis/{str(camera.uuid)}",
                json=payload,
                auth=("admin", "password")
            )

            if response.status_code == 200:
                print('mediaMTX 등록 성공')
                await self.stream_repository.insertStream(media_mtx_id=media_mtx.id, camera_id=camera.id, path_name="ANALYSIS")

            else:
                print(f'mediaMTX 등록 실패: {response.status_code} - {response.text}')

        return camera

    def update_camera(self, id, name, model, location, rtsp, is_active):
        camera = self.camera_repository.update_camera(id, name, model, location, rtsp, is_active)
        return camera