from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import List, Any

class FaceBase(BaseModel):
    name:str

class FaceCreate(FaceBase):
    image_path:str
    embedding: List[float]
    normalized_embedding:float

class FaceResponse(FaceBase):
    id: int
    name: str
    image_path: str
    embedding: List[float]
    normalized_embedding: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)