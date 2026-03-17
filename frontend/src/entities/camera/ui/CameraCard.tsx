import {useState} from "react";
import {type Camera, CameraView} from "@/entities/camera";

interface props {
    camera: Camera,
    onRefresh: () => void
}

export const CameraCard = ({ camera, onRefresh }: props) => {
    const [isProcessing, setIsProcessing] = useState(false);

    // 프로세스 제어 함수 (Start / Stop)
    const toggleCamera = async (action: 'start' | 'stop') => {
        setIsProcessing(true);
        try {
            await fetch(`${import.meta.env.VITE_API_BASE_URL}/api/v1/cameras/${camera.id}/${action}`, {
                method: 'POST'
            });
            onRefresh();
        } catch (e) {
            console.error(e)
            alert(`${action} 실패`);
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className="h-full bg-white rounded-xl overflow-hidden border border-gray-300 shadow-xl transition hover:border-gray-800/50 flex flex-col">
            {/* 상단 미리보기 영역 */}
            <div className="aspect-video bg-black relative flex items-center justify-center">
                {camera.is_active ? (
                    <CameraView
                        camId={camera.id}
                        src={`${import.meta.env.VITE_API_BASE_URL}/static/hls_output/${camera.id}/index.m3u8`}
                    />
                ) : (
                    <div className="text-gray-600 text-xs text-center">
                        <p>연결 끊김</p>
                    </div>
                )}
            </div>

            {/* 정보 영역 */}
            <div className="p-4 flex flex-col ">
                <div className="flex justify-between items-start gap-2 mb-2">
                    <h3 className="font-semibold truncate flex-1 min-w-0">
                        {camera.name}
                    </h3>
                    <span
                        className={`shrink-0 text-[10px] px-3 py-1 rounded-full ${
                            camera.is_active
                                ? 'bg-green-500/20 text-green-400'
                                : 'bg-red-500/20 text-red-400'
                        }`}
                    >
                {camera.is_active ? '실행중' : '중지됨'}
            </span>
                </div>

                <p className="text-xs text-gray-500 truncate mb-4">
                    {camera.rtsp}
                </p>

                {/* 제어 버튼 */}
                <div className="flex gap-2 mt-auto">
                    {!camera.is_active ? (
                        <button
                            onClick={() => toggleCamera('start')}
                            disabled={isProcessing}
                            className="flex-1 bg-blue-500 hover:bg-blue-600 text-white hover:text-white hover:cursor-pointer py-1.5 rounded text-xs font-medium transition"
                        >
                            {isProcessing ? '연결 중...' : '시작'}
                        </button>
                    ) : (
                        <button
                            onClick={() => toggleCamera('stop')}
                            disabled={isProcessing}
                            className="flex-1 bg-red-600/20 hover:bg-red-600 text-red-400 hover:text-white hover:cursor-pointer py-1.5 rounded text-xs font-medium transition"
                        >
                            중지
                        </button>
                    )}
                    <button className="px-3 bg-gray-200 hover:bg-gray-400 rounded text-xs transition hover:cursor-pointer">
                        설정
                    </button>
                </div>
            </div>
        </div>
    );
};