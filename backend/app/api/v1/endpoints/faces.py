import os
from typing import Optional

import cv2
import numpy as np

from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException, Depends, status
from fastapi.params import Body
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.session import async_get_db
from app.models.face import Face
from uuid import uuid4

from app.services.face_service import FaceService

UPLOAD_DIR = "static/uploads/faces"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

@router.get("/")
async def faces(db: Session = Depends(async_get_db)):
    face_service = FaceService(db)
    face_list = face_service.list_faces()

    data = [
        {
            "id": face.id,
            "name": face.name,
            "image_path": face.image_path,
            "has_embedding": face.embedding is not None,
            "normalized_embedding": face.normalized_embedding,
            "created_at": face.created_at.isoformat() if face.created_at else None,
            "updated_at": face.updated_at.isoformat() if face.updated_at else None,
        }
        for face in face_list
    ]

    return {"faces": data}

@router.post("/")
async def register_face(request: Request, name: str = Form(...), file: UploadFile = File(...), db: Session = Depends(async_get_db)):
    # 서비스 가져오기
    insightface_service = request.app.state.insightface_service
    face_service = FaceService(db)

    # 이미지 변환
    read_image = await file.read()
    np_arr = np.frombuffer(read_image, np.uint8)
    buffered_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # 얼굴 감지
    detected_faces = insightface_service.detect(buffered_image)

    if len(detected_faces) == 0:
        raise HTTPException(status_code=400, detail="감지된 얼굴이 없습니다.")

    # 이미지 저장
    file_extension = file.filename.split(".")[-1]
    file_name = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        buffer.write(read_image)

    # db 저장
    detected_face = detected_faces[0]
    embedding = detected_face.embedding
    normalized_embedding = np.linalg.norm(embedding).item()

    try:
        face = face_service.post_face(name=name, image_path=file_path, embedding=embedding, normalized_embedding=normalized_embedding)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"이미 '{name}'이라는 이름으로 등록된 얼굴 정보가 있습니다.")

    return {"id": face.id, "name": face.name, "embedding": embedding.tolist(), "normalized_embedding": face.normalized_embedding}

@router.patch("/{face_id}")
async def update_face(face_id:int, body: Optional[dict] = Body(None), db: Session = Depends(async_get_db)):
    name = body.get('name')

    face_service = FaceService(db)
    try:
        face = face_service.patch_face(face_id=face_id, name=name)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"이미 '{name}'이라는 이름으로 등록된 얼굴 정보가 있습니다.")

    return {"id": face.id, "name": face.name, "embedding": face.embedding.tolist(), "normalized_embedding": face.normalized_embedding}

@router.get("/{face_id}")
async def get_face(face_id, db: Session = Depends(async_get_db)):
    face_service = FaceService(db)
    face = face_service.get_face(face_id)

    if face is None:
        raise HTTPException(status_code=404, detail="등록된 얼굴이 없습니다.")

    return {"id": face.id, "name": face.name, "image_path": face.image_path, "created_at": face.created_at.isoformat() if face.created_at else None}

@router.delete("/{face_id}")
async def delete_face(face_id:int, db: Session = Depends(async_get_db)):
    face_service = FaceService(db)
    face = face_service.get_face(face_id)

    # 파일 삭제
    image_path = face.image_path
    os.remove(image_path)

    face_service.delete_face(face)

    return {"id": face.id, "name": face.name}