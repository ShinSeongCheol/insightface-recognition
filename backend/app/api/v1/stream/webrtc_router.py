from aiortc import RTCSessionDescription, RTCPeerConnection
from aiortc.contrib.media import MediaPlayer
from aiortc.codecs import h264
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import async_get_db

router = APIRouter()

class Offer(BaseModel):
    sdp: str
    type:str
    rtsp:str


@router.post('/')
async def web_rtc(params: Offer, db: Session = Depends(async_get_db)):

    offer = RTCSessionDescription(sdp=params.sdp, type=params.type)
    pc = RTCPeerConnection()

    transceiver = pc.addTransceiver("video", direction="sendonly")

    player = MediaPlayer(
        params.rtsp,
        options={
            "rtsp_transport": "tcp",
            "fflags": "nobuffer",
            "flags": "low_delay",
            "probesize": "32",
            "analyzeduration": "0",
            "skip_loop_filter": "all",  # CPU 절약 핵심
            "threads": "1"              # 스레드 오버헤드 방지
            # "rtsp_transport": "tcp",
            # "buffer_size": "2048000",
            # "probesize": "1000000",      # 충분한 분석
            # "analyzeduration": "1000000"
        }
    )

    if player.video:
        transceiver.sender.replaceTrack(player.video)
    else:
        print("⚠️ 경고: 비디오 트랙을 찾지 못했습니다.")

    # 5. 협상 진행
    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return {
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type
    }