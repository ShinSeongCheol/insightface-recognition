import {useCameraView} from "@/entities/model/useCameraView.ts";

export const CameraView = () => {

    const {hasError, setHasError, retryKey, streamUrl} = useCameraView()

    return (
        <div className="relative w-full h-dvh md:h-full overflow-hidden bg-black flex items-center justify-center">
            {hasError ? (
                <div className="text-center z-20">
                    <p className="text-gray-400 mb-2">카메라 연결이 원활하지 않습니다.</p>
                    <p className="text-sm text-gray-500 animate-pulse">잠시 후 다시 시도합니다...</p>
                </div>
            ) : (

                <img
                    key={retryKey}
                    src={`${streamUrl}?t=${retryKey}`}
                    alt="camera"
                    className="absolute inset-0 w-full h-full object-contain"
                    onError={() => setHasError(true)}
                />
            )}
        </div>
    );
}