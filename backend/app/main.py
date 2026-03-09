import uvicorn
import multiprocessing as mp

from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path= env_path, verbose=True)

from app.api.v1.api import api_router
from services.insightface_service import InsightfaceService
from app.db.session import engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- AI 모델(InsightFace) 로딩 시작 ---")
    insightface_service = InsightfaceService()
    app.state.insightface_service = insightface_service
    app.state.camera_processes = {}

    yield
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
    # mp.set_start_method('spawn', force=True)
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
