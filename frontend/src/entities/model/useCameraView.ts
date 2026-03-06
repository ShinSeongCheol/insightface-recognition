import {useEffect, useState} from "react";

export const useCameraView = () => {
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

    return {hasError, setHasError, retryKey, streamUrl}
}