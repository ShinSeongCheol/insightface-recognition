from sqlalchemy import Column, Integer, String, Boolean

from app.db.session import Base


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True) # camera id
    name = Column(String, nullable=False) # camera name
    model_name = Column(String) # camera model name
    location = Column(String) # camera location
    rtsp_url = Column(String, nullable=False) # camera rtsp url
    is_active = Column(Boolean, default=False) # camera active
