from app.api.v1.stream.stream_model import StreamModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Select

class StreamRepository:
    def __init__(self, db):
        self.db = db

    async def insertStream(self, media_mtx_id, camera_id, path_name) -> StreamModel:
        stream = StreamModel(media_mtx_id=media_mtx_id, camera_id=camera_id, path_name=path_name)

        try:
            self.db.add(stream)
            await self.db.commit()
            await self.db.refresh(stream)
            return stream

        except IntegrityError as e:
            self.db.rollback()
            raise e

    async def getStreamList(self):
        stmt = Select(StreamModel)
        result = self.db.execute(stmt)
        stream_list = result.scalars().all()
        return stream_list