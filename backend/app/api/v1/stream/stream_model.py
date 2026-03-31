import enum
from app.db.session import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum

class StreamType(enum.Enum):
    ORIGINAL = "original"
    ANALYSIS = "analysis"

class StreamModel(Base):
    __tablename__ = "stream"

    id = Column(Integer, primary_key=True, index=True)
    media_mtx_id = Column(Integer, ForeignKey("media_mtx.id"))
    camera_id = Column(Integer, ForeignKey("cameras.id"))
    path_name = Column(Enum(StreamType), unique=True, nullable=False)