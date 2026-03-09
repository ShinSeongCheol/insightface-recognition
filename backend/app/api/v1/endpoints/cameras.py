from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.responses import StreamingResponse
import numpy as np
import cv2
import multiprocessing as mp
from sqlalchemy.orm import Session

from app.db.session import async_get_db

def run_camera_worker(cam_id, rtsp_url):
    from app.services.camera_process import CameraProcess
    from app.services.insightface_service import InsightfaceService

    ai_service = InsightfaceService()

    worker = CameraProcess(cam_id, rtsp_url, ai_service)
    worker.run()

router = APIRouter()

@router.post("/{camera_id}/start")
async def start_camera(request: Request, camera_id:int):
    camera_processes = request.app.state.camera_processes

    # 카메라 살아있으면 오류 출력
    if camera_id in camera_processes and camera_processes[camera_id].is_alive():
        raise HTTPException(status_code=400, detail=f"Camera {camera_id} is already running")

    p = mp.Process(target=run_camera_worker, args=(camera_id, "rtsp://192.168.0.11:554/profile3/media.smp"), daemon=True)
    p.start()

    camera_processes[camera_id] = p

    return {"message": f"Camera {camera_id} started", "pid": p.pid}

@router.post("/{camera_id}/stop")
async def stop_camera(request: Request, camera_id: int):
    camera_processes = request.app.state.camera_processes

    if camera_id not in camera_processes or camera_processes[camera_id] is None:
        return {"message": f"Camera {camera_id} is not running", "status": "already_stopped"}

    p = camera_processes[camera_id]

    if p.is_alive():
        p.terminate()
        p.join(timeout=1)
        if p.is_alive():
            p.kill()

    camera_processes.pop(camera_id, None)

    return {"message": f"Camera {camera_id} stopped successfully"}
