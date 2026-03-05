from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.access_log import AccessLog

class AccessLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, face_id, image_path: str):
        access_log = AccessLog(face_id=face_id, image_path=image_path)
        try:
            self.db.add(access_log)
            self.db.commit()
            self.db.refresh(access_log)
        except IntegrityError as e:
            self.db.rollback()
            raise e

        return access_log