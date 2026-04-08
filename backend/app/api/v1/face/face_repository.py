from sqlalchemy.sql import select
from app.api.v1.face.face_model import FaceModel
from sqlalchemy.exc import IntegrityError

from app.api.v1.face.face_schema import FaceCreate


class FaceRepository:
    def __init__(self, db):
        self.db = db

    async def get_face_list(self):
        stmt = select(FaceModel)
        result = await self.db.execute(stmt)
        faces = result.scalars().all()
        return faces

    async def get_face(self, face_id):
        stmt = select(FaceModel).where(FaceModel.id == int(face_id))
        result = await self.db.execute(stmt)
        face = result.scalars().first()
        return face

    async def post_face(self, requested_face:FaceCreate) -> FaceModel:
        face = FaceModel(**requested_face.model_dump())

        try:
            self.db.add(face)
            await self.db.commit()
            await self.db.refresh(face)
            return face

        except IntegrityError as e:
            self.db.rollback()
            raise e

    async def patch_face(self, face_id, name):
        stmt = select(FaceModel).where(FaceModel.id == int(face_id))
        result = await self.db.execute(stmt)
        face = result.scalars().first()
        face.name = name

        try:
            self.db.add(face)
            await self.db.commit()
            await self.db.refresh(face)
            return face

        except IntegrityError as e:
            self.db.rollback()
            raise e


    async def delete_face(self, face: FaceModel):
        await self.db.delete(face)
        await self.db.commit()