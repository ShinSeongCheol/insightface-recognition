from sqlalchemy.sql import select

from app.api.v1.snapshot.snapshot_model import SnapshotModel


class SnapshotRepository:
    def __init__(self, db):
        self.db = db

    def list_snapshots(self):
        stmt = select(Snapshot)
        result = self.db.execute(stmt)
        snapshot_list = result.scalars().all()
        return snapshot_list

    def save(self, face_id, image_path: str):
        snapshot = Snapshot(face_id=face_id, image_path=image_path)
        try:
            self.db.add(snapshot)
            self.db.commit()
            self.db.refresh(snapshot)
        except IntegrityError as e:
            self.db.rollback()
            raise e

        return snapshot