from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class CameraBase(BaseModel):
    name: str
    model_name:str
    location:str
    rtsp_url:str

class CameraRequest(CameraBase):
    uuid: UUID = Field(default_factory=uuid4)

class CameraResponse(CameraBase):
    id: int
    uuid: str