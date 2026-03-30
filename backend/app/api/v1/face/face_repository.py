from sqlalchemy.sql import select
from app.api.v1.face.face_model import FaceModel
from sqlalchemy.exc import IntegrityError

from app.api.v1.face.face_schema import FaceCreate


class FaceRepository:
    def __init__(self, db):
        self.db = db

    def get_face_list(self):
        stmt = select(FaceModel)
        result = self.db.execute(stmt)
        faces = result.scalars().all()
        return faces

    def get_face(self, face_id):
        stmt = select(FaceModel).where(FaceModel.id == face_id)
        face = self.db.execute(stmt).scalars().first()
        return face

    def post_face(self, requested_face:FaceCreate) -> FaceModel:
        face = FaceModel(**requested_face.model_dump())

        try:
            self.db.add(face)
            self.db.commit()
            self.db.refresh(face)
            return face

        except IntegrityError as e:
            self.db.rollback()
            raise e

    def patch_face(self, face_id, name):
        stmt = select(FaceModel).where(FaceModel.id == face_id)
        face = self.db.execute(stmt).scalars().first()
        face.name = name

        try:
            self.db.add(face)
            self.db.commit()
            self.db.refresh(face)
            return face

        except IntegrityError as e:
            self.db.rollback()
            raise e


    def delete_face(self, face: FaceModel):
        self.db.delete(face)
        self.db.commit()