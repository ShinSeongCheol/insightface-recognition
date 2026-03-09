import { useEffect, useRef } from "react";
import Hls from "hls.js";

export const useCameraView = ({ src }: { src: string }) => {
    const videoRef = useRef<HTMLVideoElement>(null);

    useEffect(() => {
        const video = videoRef.current;
        if (!video) return; // 엘리먼트가 없으면 아무것도 안 함

        let hls: Hls;

        if (Hls.isSupported()) {
            hls = new Hls({
                maxBufferLength: 10,
                maxMaxBufferLength: 20,
                enableWorker: true,
                lowLatencyMode: true,
            });

            hls.loadSource(src);
            hls.attachMedia(video);

            hls.on(Hls.Events.MANIFEST_PARSED, () => {
                // 브라우저 정책상 muted 상태여야 자동 재생이 잘 됩니다.
                video.play().catch((e) => console.log("Autoplay blocked:", e));
            });

            hls.on(Hls.Events.ERROR, (_event, data) => {
                if (data.fatal) {
                    switch (data.type) {
                        case Hls.ErrorTypes.NETWORK_ERROR:
                            hls.startLoad();
                            break;
                        case Hls.ErrorTypes.MEDIA_ERROR:
                            hls.recoverMediaError();
                            break;
                        default:
                            hls.destroy();
                            break;
                    }
                }
            });
        }
        // 2. Safari 등 HLS를 네이티브로 지원하는 경우 (video 타입 체크 덕분에 에러 안 남)
        else if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = src;
        }

        return () => {
            if (hls) {
                hls.destroy();
            }
        };
    }, [src]);

    return { videoRef };
};