from app.repositories.snapshot_repository import SnapshotRepository


class SnapshotService:
    def __init__(self, db):
        self.db = db
        self.snapshot_repository = SnapshotRepository(db)

    def list_snapshots(self):
        snapshots = self.snapshot_repository.list_snapshots()
        return snapshots