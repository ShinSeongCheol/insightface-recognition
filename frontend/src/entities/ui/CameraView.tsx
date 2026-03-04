import {useEffect, useState} from "react";

export const CameraView = () => {
    const [hasError, setHasError] = useState(false);
    const [retryKey, setRetryKey] = useState(0); // 재연결을 강제하기 위한 키

    const streamUrl = `${import.meta.env.VITE_API_BASE_URL}/api/v1/cameras/stream`;

    // 에러 발생 시 3초 후 재연결 시도
    useEffect(() => {
        let timer: number;
        if (hasError) {
            timer = window.setTimeout(() => {
                setHasError(false);
                setRetryKey(prev => prev + 1);
            }, 3000);
        }
        return () => clearTimeout(timer);
    }, [hasError]);

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