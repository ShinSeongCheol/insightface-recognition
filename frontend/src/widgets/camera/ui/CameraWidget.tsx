import {CameraCard} from "@/entities/camera/ui/CameraCard.tsx";
import {useEffect, useState} from "react";
import {type Camera, fetchCameraList} from "@/entities/camera";
import {CreateCameraCardButton} from "@features/camera";

export const CameraWidget = () => {
    const [cameras, setCameras] = useState<Camera[]>([]);
    const [loading, setLoading] = useState(true);

    const load = async () => {
        try {
            const res = await fetchCameraList();
            setCameras(res.cameras);
        }catch (e){
            console.error(e)
        }finally {
            setLoading(false)
        }
    };

    useEffect(() => {
        load();
        const timer = setInterval(load, 1000 * 10);
        return () => clearInterval(timer);
    }, []);

    return (
        <div className="min-h-screen bg-white p-6 text-black">
            {/* 상단 헤더 */}
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-2xl font-bold">카메라 관리 시스템</h1>
                    <p className="text-gray-400 text-sm">전체 {cameras.length}대의 카메라가 등록되어 있습니다.</p>
                </div>
            </div>

            {/* 카메라 그리드 리스트 */}
            {loading ?
                <div>로딩중입니다.</div>
                :
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 items-stretch">
                    {cameras.sort((a,b) => a.id - b.id).map((cam) => (
                        <CameraCard
                            key={cam.id}
                            camera={cam}
                            onRefresh={load}
                        />
                    ))}
                    <CreateCameraCardButton/>
                </div>
            }
        </div>
    )
}