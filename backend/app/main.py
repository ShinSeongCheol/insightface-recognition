from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path= env_path, verbose=True)

import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.api.v1.mediaMtx.mediaMtx_service import MediaMtxService
from app.api.v1.stream.stream_service import StreamService

from app.api.v1.api import api_router
from app.api.v1.insightface.insightface_service import InsightfaceService
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import async_get_db, AsyncSessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    insightface_service = InsightfaceService()
    app.state.insightface_service = insightface_service
    app.state.stream_service = StreamService(insightface_service, AsyncSessionLocal)
    app.state.mediaMtx_service = MediaMtxService(session_factory=AsyncSessionLocal)

    await app.state.mediaMtx_service.init()

    await app.state.stream_service.init()

    yield
    del app.state.insightface_service

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
