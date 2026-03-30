from sqlalchemy import Column, Integer, String, Boolean

from app.db.session import Base


class CameraModel(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True) # camera id
    code = Column(String, nullable=False, unique=True) # camera code
    name = Column(String, nullable=False) # camera name
    model_name = Column(String) # camera model name
    location = Column(String) # camera location
    rtsp_url = Column(String, nullable=False) # camera rtsp url
