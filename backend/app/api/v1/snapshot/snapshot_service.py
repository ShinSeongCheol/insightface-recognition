from app.api.v1.snapshot.snapshot_repository import SnapshotRepository


class SnapshotService:
    def __init__(self, db):
        self.db = db
        self.snapshot_repository = SnapshotRepository(db)

    async def list_snapshots(self):
        snapshots = await self.snapshot_repository.list_snapshots()
        return snapshots