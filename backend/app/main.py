from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path= env_path, verbose=True)

from app.api.v1.api import api_router
from app.services.camera_service import CameraService
from services.insightface_service import InsightfaceService
from app.db.session import engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- AI 모델(InsightFace) 로딩 시작 ---")
    insightface_service = InsightfaceService()
    app.state.insightface_service = insightface_service

    print("--- 카메라 로딩 시작 ---")
    camera_service = CameraService(insightface_service)
    camera_service.start()

    app.state.camera_service = camera_service

    yield
    camera_service.stop()
    del insightface_service

app = FastAPI(lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 테스트 중엔 모든 주소 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
