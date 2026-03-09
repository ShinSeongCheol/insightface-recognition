import {useCameraView} from "@/entities/camera/model/useCameraView.ts";

export const CameraView = () => {
    const camId = 1;
    const { videoRef } = useCameraView({
        src: `${import.meta.env.VITE_API_BASE_URL}/static/hls_output/1/index.m3u8`
    });

    return (
        <div className="relative w-full h-dvh md:h-full overflow-hidden bg-black flex items-center justify-center">
            <video
                ref={videoRef}
                muted
                autoPlay
                playsInline
                className="object-cover"
            />
            <div className="absolute top-2 left-2 z-10 bg-black/50 px-2 py-1 rounded text-white text-[10px] backdrop-blur-sm">
                CAM {camId}
            </div>
        </div>
    );
}