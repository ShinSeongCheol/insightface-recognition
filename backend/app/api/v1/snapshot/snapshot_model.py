from app.db.session import Base
from sqlalchemy import Integer, Column, ForeignKey, DateTime, String
from datetime import datetime

class SnapshotModel(Base):
    __tablename__ = "snapshot"
    id = Column(Integer, primary_key=True)
    face_id = Column(Integer, ForeignKey("faces.id"), nullable=True)
    image_path = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.now())