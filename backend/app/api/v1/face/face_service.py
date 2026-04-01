import os
import numpy as np
import cv2
from uuid import uuid4

from app.api.v1.face.face_repository import FaceRepository
from app.api.v1.face.face_schema import FaceCreate
from app.api.v1.insightface.insightface_service import InsightfaceService
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException,status


class FaceService:
    def __init__(self, db, insightface_service: InsightfaceService = None):
        self.db = db
        self.face_repository = FaceRepository(db)
        self.insightface_service = insightface_service
        self.upload_dir = "app/static/uploads/faces"

    async def get_face_list(self):
        face_list = self.face_repository.get_face_list()
        return face_list

    async def get_face(self, face_id):
        face = self.face_repository.get_face(face_id)
        return face

    async def post_face(self, name, file):
        # 이미지 변환
        read_image = await file.read()
        np_arr = np.frombuffer(read_image, np.uint8)
        buffered_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if buffered_image is None:
            raise HTTPException(status_code=400, detail="유효하지 않은 이미지 파일입니다.")

        # 얼굴 감지
        detected_faces = self.insightface_service.detect(buffered_image)

        if len(detected_faces) == 0:
            raise HTTPException(status_code=400, detail="감지된 얼굴이 없습니다.")

        # db 저장
        detected_face = detected_faces[0]
        embedding = detected_face.embedding
        normalized_embedding = np.linalg.norm(embedding).item()

        file_extension = file.filename.split(".")[-1]
        file_name = f"{uuid4()}.{file_extension}"
        image_path = os.path.join(self.upload_dir, file_name)

        requested_face = FaceCreate(
            name=name,
            image_path=image_path,
            embedding=embedding,
            normalized_embedding=normalized_embedding
        )
        try:
            face = self.face_repository.post_face(requested_face)

            # 이미지 저장
            os.makedirs(self.upload_dir, exist_ok=True)

            with open(image_path, "wb") as buffer:
                buffer.write(read_image)

            return face
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"이미 '{name}'이라는 이름으로 등록된 얼굴 정보가 있습니다.")

    async def patch_face(self, face_id, name):
        try:
            face = self.face_repository.patch_face(face_id, name)
            return face
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"이미 '{name}'이라는 이름으로 등록된 얼굴 정보가 있습니다.")

    async def delete_face(self, face_id):
        face = self.get_face(face_id)

        # 파일 삭제
        image_path = face.image_path
        os.remove(image_path)

        self.face_repository.delete_face(face)
