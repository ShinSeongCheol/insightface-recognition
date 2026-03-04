from threading import Thread
from PIL import Image, ImageDraw, ImageFont
import os
import cv2
import numpy as np


class CameraService:
    def __init__(self):
        self.running = False
        self.thread = None
        self.frame = None

    def start(self):
        self.running = True
        self.thread = Thread(target=self.loop, args=(), daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def read(self) -> np.ndarray:
        return self.frame

    def loop(self):
        rtsp_url = "rtsp://192.168.0.11:554/profile3/media.smp"
        cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                continue
            self.frame = frame

        cap.release()

    def draw_korean_text_bgr(
            self,
            bgr: np.ndarray,
            text: str,
            org: tuple[int, int],
            font_path: str = "C:/Windows/Fonts/malgun.ttf",
            font_size: int = 20,
            color_bgr=(0, 0, 255),
    ):
        # 1) BGR -> RGB
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)

        # 2) 폰트 로드(실패 시 대체 경로도 시도)
        if not os.path.exists(font_path):
            # 윈도우에서 대체 후보
            for fp in ["C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf", "C:/Windows/Fonts/gulim.ttc"]:
                if os.path.exists(fp):
                    font_path = fp
                    break

        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception:
            # 기본 폰트는 한글이 안 나올 수 있음
            font = ImageFont.load_default()

        draw = ImageDraw.Draw(pil_img)

        # 3) PIL은 RGB 컬러
        color_rgb = (color_bgr[2], color_bgr[1], color_bgr[0])
        draw.text(org, text, font=font, fill=color_rgb)

        # 4) RGB -> BGR
        out = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        return out