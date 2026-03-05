from sqlalchemy.sql import select
from app.models.face import Face
from sqlalchemy.exc import IntegrityError

class FaceService:
    def __init__(self, db):
        self.db = db

    def list_faces(self):
        stmt = select(Face)
        result = self.db.execute(stmt)
        faces = result.scalars().all()
        return faces

    def get_face(self, face_id):
        stmt = select(Face).where(Face.id == face_id)
        face = self.db.execute(stmt).scalars().first()
        return face

    def post_face(self, name, image_path, embedding, normalized_embedding):
        face = Face(name=name, image_path=image_path, embedding=embedding, normalized_embedding=normalized_embedding)

        try:
            self.db.add(face)
            self.db.commit()
            self.db.refresh(face)
        except IntegrityError as e:
            self.db.rollback()
            raise e

        return face

    def patch_face(self, face_id, name):
        stmt = select(Face).where(Face.id == face_id)
        face = self.db.execute(stmt).scalars().first()
        face.name = name

        try:
            self.db.add(face)
            self.db.commit()
            self.db.refresh(face)
        except IntegrityError as e:
            self.db.rollback()
            raise e

        return face

    def delete_face(self, face: Face):
        self.db.delete(face)
        self.db.commit()