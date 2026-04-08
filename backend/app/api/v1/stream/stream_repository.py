from typing import List, Tuple

from app.api.v1.camera.camera_model import CameraModel
from app.api.v1.mediaMtx.mediaMtx_model import MediaMtxModel
from app.api.v1.stream.stream_model import StreamModel, StreamType
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

    async def getStreamList(self) -> List[StreamModel]:
        stmt = Select(StreamModel)
        result = await self.db.execute(stmt)
        stream_list = result.scalars().all()
        return stream_list

    async def getAnaysisStreamInfoList(self) -> List[Tuple[StreamModel, CameraModel, MediaMtxModel]]:
        stmt = (
            Select(StreamModel, CameraModel, MediaMtxModel)
            .where(StreamModel.path_name == StreamType.ANALYSIS)
            .join(CameraModel, StreamModel.camera_id == CameraModel.id)
            .join(MediaMtxModel, MediaMtxModel.id == StreamModel.media_mtx_id)
        )

        result = await self.db.execute(stmt)
        return result.all()