from app.models.face import Face

from app.repositories.face_repository import FaceRepository


class FaceService:
    def __init__(self, db):
        self.db = db
        self.face_repository = FaceRepository(db)

    def list_faces(self):
        faces = self.face_repository.list_faces()
        return faces

    def get_face(self, face_id):
        face = self.face_repository.get_face(face_id)
        return face

    def post_face(self, name, image_path, embedding, normalized_embedding):
        face = self.face_repository.post_face(name=name, image_path=image_path, embedding=embedding, normalized_embedding=normalized_embedding)
        return face

    def patch_face(self, face_id, name):
        face = self.face_repository.patch_face(face_id, name)
        return face

    def delete_face(self, face: Face):
        self.face_repository.delete_face(face)