from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import async_get_db
from app.services.snapshot_service import SnapshotService

router = APIRouter()

@router.get("/")
async def faces(db: Session = Depends(async_get_db)):

    snapshot_service = SnapshotService(db)
    snapshots = snapshot_service.list_snapshots()

    data = [
        {
            "id": snapshot.id,
            "image_path": snapshot.image_path,
            "timestamp": snapshot.timestamp,
        }
        for snapshot in snapshots
    ]

    return {"snapshots": data}