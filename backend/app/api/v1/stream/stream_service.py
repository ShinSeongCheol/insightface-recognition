import asyncio
import multiprocessing as mp
import cv2
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.stream.stream_repository import StreamRepository


class StreamService:
    def __init__(self, insightface_service, session_factory):
        self.insightface_service = insightface_service
        self.session_factory = session_factory
        self.running_tasks = []

    async def init(self):
        async with self.session_factory() as db:
            stream_repository = StreamRepository(db)
            analysis_stream_info_list = await stream_repository.getAnaysisStreamInfoList()

            for stream, camera, mediamtx in analysis_stream_info_list:
                task = asyncio.create_task(self.start_analysis(stream, camera, mediamtx))
                self.running_tasks.append(task)

            if self.running_tasks:
                await asyncio.gather(*self.running_tasks)

    async def start_analysis(self, stream, camera, mediamtx):
        raw_q = mp.Queue(maxsize=1)
        result_q = mp.Queue(maxsize=1)

        proc = mp.Process(
            target=self._processing_worker,
            args=(raw_q, result_q,), # 예시: 설정값만 전달
            daemon=True
        )
        proc.start()

        try:
            await asyncio.gather(
                self._receive_video(stream, camera, raw_q),
                self._transmit_video(result_q, mediamtx)
            )
        finally:
            proc.terminate()
            proc.join()

    async def _receive_video(self, stream, camera, raw_q):
        cap = cv2.VideoCapture(camera.rtsp_url)
        while True:
            ret, frame = await asyncio.to_thread(cap.read)
            if not ret:
                # 연결 끊김 시 재시도 로직
                await asyncio.sleep(5)
                cap.open(camera.rtsp_url)
                continue

            if raw_q.full():
                try: raw_q.get_nowait()
                except: pass
            raw_q.put(frame)
            await asyncio.sleep(0.01)

    @staticmethod
    def _processing_worker(raw_q, result_q):
        from app.api.v1.insightface.insightface_service import InsightfaceService
        model = InsightfaceService()

        while True:
            frame = raw_q.get()
            results = model.detect(frame)

            if result_q.full():
                try: result_q.get_nowait()
                except: pass
            result_q.put((frame, results))

    async def _transmit_video(self, result_q, mediamtx):
        while True:
            frame, results = await asyncio.to_thread(result_q.get)
            print(frame)
            await asyncio.sleep(0.01)