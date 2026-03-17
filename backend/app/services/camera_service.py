from skimage.data import camera

from app.repositories.camera_repository import CameraRepository
from app.models.camera import Camera

class CameraService:
    def __init__(self, db):
        self.db = db
        self.camera_repository = CameraRepository(db)

    def list_camera(self):
        cameras = self.camera_repository.list_cameras()
        return cameras

    def select_camera(self, id):
        camera = self.camera_repository.select_camera(id)
        return camera

    def insert_camera(self, data):
        name = data['name']
        model = data['model']
        location = data['location']
        rtsp = data['rtsp']

        camera = self.camera_repository.insert_camera(name=name, model=model, location=location, rtsp=rtsp)
        return camera

    def update_camera(self, id, name, model, location, rtsp, is_active):
        camera = self.camera_repository.update_camera(id, name, model, location, rtsp, is_active)
        return camera
