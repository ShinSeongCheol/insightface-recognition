from app.db.session import Base
from sqlalchemy import Column, Integer, String

class MediaMtxModel(Base):
    __tablename__ = "media_mtx"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, nullable=False, unique=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)
    rtsp_port = Column(Integer)
    hls_port = Column(Integer)
    webrtc_port = Column(Integer)
    api_port = Column(Integer)