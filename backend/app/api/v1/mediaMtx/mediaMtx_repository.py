from sqlalchemy.sql import select
from app.api.v1.mediaMtx.mediaMtx_model import MediaMtxModel

class MediaMtxRepository:
    def __init__(self, db):
        self.db = db

    async def getMediaMtx(self, media_mtx_id) -> MediaMtxModel:
        stmt = select(MediaMtxModel).where(MediaMtxModel.id == media_mtx_id)
        media_mtx = self.db.execute(stmt).scalars().first()
        return media_mtx