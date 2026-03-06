from sqlalchemy.sql import select

from app.models.access_log import AccessLog


class SnapshotRepository:
    def __init__(self, db):
        self.db = db

    def list_snapshots(self):
        stmt = select(AccessLog)
        result = self.db.execute(stmt)
        accessLogs = result.scalars().all()
        return accessLogs