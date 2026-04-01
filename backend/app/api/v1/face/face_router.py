import os
from typing import Optional, List, Dict

from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session

from app.api.v1.face.face_schema import FaceResponse
from app.db.session import async_get_db

from app.api.v1.face.face_service import FaceService

router = APIRouter()

@router.get("/", response_model=Dict[str, List[FaceResponse]])
async def faces(db: Session = Depends(async_get_db)):
    face_service = FaceService(db)
    face_list = await face_service.get_face_list()

    return {"faces":face_list}

@router.post("/", response_model=FaceResponse)
async def register_face(request: Request, name: str = Form(...), file: UploadFile = File(...), db: Session = Depends(async_get_db)):
    # 서비스 가져오기
    insightface_service = request.app.state.insightface_service

    face_service = FaceService(db, insightface_service)
    face = await face_service.post_face(name=name, file=file)

    return face

@router.patch("/{face_id}", response_model=FaceResponse)
async def update_face(face_id:int, body: Optional[dict] = Body(None), db: Session = Depends(async_get_db)):
    name = body.get('name')

    face_service = FaceService(db)
    face = await face_service.patch_face(face_id=face_id, name=name)

    return face

@router.get("/{face_id}", response_model=FaceResponse)
async def get_face(face_id, db: Session = Depends(async_get_db)):
    face_service = FaceService(db)
    face = await face_service.get_face(face_id)

    if face is None:
        raise HTTPException(status_code=404, detail="등록된 얼굴이 없습니다.")

    return face

@router.delete("/{face_id}")
async def delete_face(face_id:int, db: Session = Depends(async_get_db)):
    face_service = FaceService(db)

    await face_service.delete_face(face_id)

    return {"id": face_id}