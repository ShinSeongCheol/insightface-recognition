from sqlalchemy.sql import select

from app.api.v1.snapshot.snapshot_model import SnapshotModel


class SnapshotRepository:
    def __init__(self, db):
        self.db = db

    async def list_snapshots(self):
        stmt = select(SnapshotModel)
        result = await self.db.execute(stmt)
        snapshot_list = result.scalars().all()
        return snapshot_list

    async def save(self, face_id, image_path: str):
        snapshot = SnapshotModel(face_id=face_id, image_path=image_path)
        try:
            self.db.add(snapshot)
            await self.db.commit()
            await self.db.refresh(snapshot)
        except IntegrityError as e:
            self.db.rollback()
            raise e

        return snapshot