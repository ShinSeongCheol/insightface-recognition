from sqlalchemy.orm import Session

class AccessLogService:
    def __init__(self, db: Session):
        self.db = db

    def save_access_log(self):
        pass
