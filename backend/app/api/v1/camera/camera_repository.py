from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from app.api.v1.camera.camera_model import CameraModel
from app.api.v1.camera.camera_schema import CameraRequest


class CameraRepository:
    def __init__(self, db):
        self.db: Session = db

    async def list_cameras(self):
        stmt = select(CameraModel)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def select_camera(self, id):
        stmt = select(CameraModel).where(CameraModel.id == id)
        camera = await self.db.execute(stmt)
        return camera.scalars().first()

    async def insert_camera(self, camera: CameraRequest) -> CameraModel:
        new_camera = CameraModel(**camera.model_dump())
        try:
            self.db.add(new_camera)
            await self.db.commit()
            await self.db.refresh(new_camera)
        except InterruptedError as e:
            self.db.rollback()
            raise e

        return new_camera

    async def update_camera(self, id, name, model, location, rtsp, is_active):
        stmt = select(CameraModel).where(CameraModel.id == id)
        result = self.db.execute(stmt)

        camera: CameraModel = result.scalars().first()
        camera.name = name
        camera.model_name = model
        camera.location = location
        camera.rtsp_url = rtsp
        camera.is_active = is_active

        try:
            self.db.add(camera)
            await self.db.commit()
            await self.db.refresh(camera)
        except IntegrityError as e:
            self.db.rollback()
            raise e

        return camera

    def delete_camera(self, camera):
        pass