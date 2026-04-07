import asyncio

import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path= env_path, verbose=True)

from app.api.v1.mediaMtx.mediaMtx_model import MediaMtxModel
from app.api.v1.mediaMtx.mediaMtx_repository import MediaMtxRepository
from app.api.v1.stream.stream_model import StreamModel
from app.api.v1.stream.stream_repository import StreamRepository
from app.api.v1.camera.camera_repository import CameraRepository

import httpx

from app.api.v1.api import api_router
from app.api.v1.insightface.insightface_service import InsightfaceService
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import async_get_db

async def _sync_mediamtx():
    print("[Sync] 태스크가 시작되었습니다.") # 시작 확인용

    try:
        # 1. DB 세션 수동 획득 (제너레이터 방식 대응)
        async for db in async_get_db():
            print("[Sync] DB 세션 획득 성공")

            try:
                # 2. 반드시 await 확인! (Repository 메서드가 async인 경우)
                # 만약 async 함수가 아니라면 await를 제거하세요.
                media_mtx = await MediaMtxRepository(db).getMediaMtx(1)
                print(f"[Sync] MediaMTX 정보 로드 완료: {media_mtx}")

                stream_list = await StreamRepository(db).getStreamList()

                # --- 이후 MediaMTX 통신 로직 ---
                async with httpx.AsyncClient() as client:
                    for stream in stream_list:
                        camera = await CameraRepository(db).select_camera(stream.camera_id)
                        original_url = f"http://{media_mtx.ip}:{media_mtx.api_port}/v3/config/paths/add/original/{str(camera.uuid)}"
                        analysis_url = f"http://{media_mtx.ip}:{media_mtx.api_port}/v3/config/paths/add/analysis/{str(camera.uuid)}"

                        from app.api.v1.stream.stream_model import StreamType
                        if stream.path_name == StreamType.ORIGINAL:
                            payload = {
                                "name": "original/" +  str(camera.uuid),
                                "source": camera.rtsp_url,
                                "sourceOnDemand": True
                            }

                            response = await client.post(
                                original_url,
                                json=payload,
                                auth=("admin", "password")
                            )

                            if response.status_code == 200:
                                print('mediaMTX 등록 성공')

                            else:
                                print(f'mediaMTX 등록 실패: {response.status_code} - {response.text}')
                        elif stream.path_name == StreamType.ANALYSIS:
                            payload = {
                                "name": "analysis/" +  str(camera.uuid),
                                "source": "publisher",
                            }

                            response = await client.post(
                                analysis_url,
                                json=payload,
                                auth=("admin", "password")
                            )

                            if response.status_code == 200:
                                print('mediaMTX 등록 성공')

                            else:
                                print(f'mediaMTX 등록 실패: {response.status_code} - {response.text}')


            except Exception as e:
                print("--- Repository 또는 로직 에러 발생 ---")
                print(e)

    except Exception as e:
        print("--- DB 세션 획득 실패 또는 태스크 초기 에러 ---")
        print(e)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.insightface_service = InsightfaceService()
    sync_mediamtx = asyncio.create_task(_sync_mediamtx())
    yield
    del app.state.insightface_service
    sync_mediamtx.cancel()

app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 테스트 중엔 모든 주소 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    # mp.set_start_method('spawn', force=True)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
