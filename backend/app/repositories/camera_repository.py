from skimage.data import camera
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from app.models.camera import Camera

class CameraRepository:
    def __init__(self, db):
        self.db: Session = db

    def list_cameras(self):
        stmt = select(Camera)
        result = self.db.execute(stmt).scalars().all()
        return result

    def select_camera(self, id):
        stmt = select(Camera).where(Camera.id == id)
        camera = self.db.execute(stmt).scalars().first()
        return camera

    def insert_camera(self, name, model, location, rtsp):
        camera = Camera(name=name, model_name=model, location=location, rtsp_url=rtsp)
        try:
            self.db.add(camera)
            self.db.commit()
            self.db.refresh(camera)
        except InterruptedError as e:
            self.db.rollback()
            raise e

        return camera

    def update_camera(self, id, name, model, location, rtsp, is_active):
        stmt = select(Camera).where(Camera.id == id)
        camera: Camera = self.db.execute(stmt).scalars().first()
        camera.name = name
        camera.model_name = model
        camera.location = location
        camera.rtsp_url = rtsp
        camera.is_active = is_active

        try:
            self.db.add(camera)
            self.db.commit()
            self.db.refresh(camera)
        except IntegrityError as e:
            self.db.rollback()
            raise e

        return camera

    def delete_camera(self, camera):
        pass