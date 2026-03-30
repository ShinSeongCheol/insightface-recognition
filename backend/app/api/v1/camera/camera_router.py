from fastapi import APIRouter, Request, Depends, HTTPException
import multiprocessing as mp
from sqlalchemy.orm import Session

from app.db.session import async_get_db
from app.api.v1.camera.camera_service import CameraService


def run_camera_worker(cam_id, rtsp_url):
    from app.services.camera_process import CameraProcess
    from app.api.v1.insightface.insightface_service import InsightfaceService

    ai_service = InsightfaceService()

    worker = CameraProcess(cam_id, rtsp_url, ai_service)
    worker.run()

router = APIRouter()

@router.get("/")
async def list_cameras(db: Session = Depends(async_get_db)):
    camera_service = CameraService(db)
    cameras = camera_service.list_camera()

    data = [
        {
            "id": camera.id,
            "name": camera.name,
            "model_name": camera.model_name,
            "location": camera.location,
            "rtsp_url": camera.rtsp_url,
            "is_active": camera.is_active
        }
        for camera in cameras
    ]

    return {
        "cameras": data
    }

@router.post("/")
async def insert_camera(request: Request, db: Session = Depends(async_get_db)):
    data = await request.json()

    camera_service = CameraService(db)
    camera = camera_service.insert_camera(data)
    return {"data": camera}

@router.patch("/{camera_id}")
async def update_camera(request: Request, camera_id: int):
    pass

@router.delete("/{camera_id}")
async def delete_camera(request: Request, camera_id: int):
    pass

@router.post("/{camera_id}/start")
async def start_camera(request: Request, camera_id:int, db: Session = Depends(async_get_db)):
    camera_processes = request.app.state.camera_processes

    # 카메라 살아있으면 오류 출력
    if camera_id in camera_processes and camera_processes[camera_id].is_alive():
        raise HTTPException(status_code=400, detail=f"Camera {camera_id} is already running")



    camera_service = CameraService(db)
    camera= camera_service.select_camera(camera_id)

    p = mp.Process(target=run_camera_worker, args=(camera_id, camera.rtsp_url), daemon=True)
    p.start()

    camera_processes[camera_id] = p

    updated_camera = camera_service.update_camera(camera.id, camera.name, camera.model_name, camera.location, camera.rtsp_url, True)

    return {"message": f"Camera {updated_camera.id} started", "pid": p.pid}

@router.post("/{camera_id}/stop")
async def stop_camera(request: Request, camera_id: int, db:Session = Depends(async_get_db)):
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

    camera_service = CameraService(db)
    camera= camera_service.select_camera(camera_id)

    updated_camera = camera_service.update_camera(camera.id, camera.name, camera.model_name, camera.location, camera.rtsp_url, False)

    return {"message": f"Camera {camera_id} stopped successfully"}
