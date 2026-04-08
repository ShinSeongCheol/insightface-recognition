import httpx

from app.api.v1.camera.camera_model import CameraModel
from app.api.v1.camera.camera_repository import CameraRepository
from app.api.v1.mediaMtx.mediaMtx_repository import MediaMtxRepository
from app.api.v1.stream.stream_repository import StreamRepository

from app.api.v1.stream.stream_model import StreamType

class MediaMtxService:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def init(self):
        async with self.session_factory() as db:
            print("[Sync] DB 세션 획득 성공")
            try:
                media_mtx = await MediaMtxRepository(db).getMediaMtx(1)
                stream_list = await StreamRepository(db).getStreamList()

                for stream in stream_list:
                    camera = await CameraRepository(db).select_camera(stream.camera_id)
                    original_url = f"http://{media_mtx.ip}:{media_mtx.api_port}/v3/config/paths/add/original/{str(camera.uuid)}"
                    analysis_url = f"http://{media_mtx.ip}:{media_mtx.api_port}/v3/config/paths/add/analysis/{str(camera.uuid)}"

                    if stream.path_name == StreamType.ORIGINAL:
                        await self.start_original_stream(camera)
                    elif stream.path_name == StreamType.ANALYSIS:
                        await self.start_analysis_stream(camera)

            except Exception as e:
                print("--- Repository 또는 로직 에러 발생 ---")
                print(e)

    async def start_original_stream(self, camera:CameraModel):
        async with self.session_factory() as db:
            media_mtx = await MediaMtxRepository(db).getMediaMtx(1)
            stream_repository = StreamRepository(db)
            async with httpx.AsyncClient() as client:
                payload = {
                    "name": "original/" +  str(camera.uuid),
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
                    await stream_repository.insertStream(media_mtx_id=media_mtx.id, camera_id=camera.id, path_name="ORIGINAL")

                else:
                    print(f'mediaMTX 등록 실패: {response.status_code} - {response.text}')

    async def start_analysis_stream(self, camera):
        async with self.session_factory() as db:
            media_mtx = await MediaMtxRepository(db).getMediaMtx(1)
            stream_repository = StreamRepository(db)
            async with httpx.AsyncClient() as client:
                payload = {
                    "name": "analysis/" +  str(camera.uuid),
                    "source": "publisher",
                }

                response = await client.post(
                    f"http://{media_mtx.ip}:{media_mtx.api_port}/v3/config/paths/add/analysis/{str(camera.uuid)}",
                    json=payload,
                    auth=("admin", "password")
                )

                if response.status_code == 200:
                    print('mediaMTX 등록 성공')
                    await stream_repository.insertStream(media_mtx_id=media_mtx.id, camera_id=camera.id, path_name="ANALYSIS")

                else:
                    print(f'mediaMTX 등록 실패: {response.status_code} - {response.text}')