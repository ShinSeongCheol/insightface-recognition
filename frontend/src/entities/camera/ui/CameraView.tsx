import {useCameraView} from "@/entities/camera/model/useCameraView.ts";

export const CameraView = ({camId, src} : {camId: number, src: string}) => {
    const { videoRef } = useCameraView({
        src: src
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