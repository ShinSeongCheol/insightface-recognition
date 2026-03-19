import {useCameraGridViewWidget} from "@/widgets/camera/model/useCameraGridViewWidget.ts";
import {CameraView} from "@/entities/camera";

export const CameraGridViewWidget = () => {
    const {cameras, isLoading} = useCameraGridViewWidget();

    return (
        <div className={'grid grid-cols-1 lg:grid-cols-2 gap-2 p-2'}>
            {isLoading ?
                <div>로딩중 입니다.</div>
                :
                cameras.sort((a,b) => a.id - b.id).filter((camera) => camera.is_active === true).map((camera) => {
                    return <CameraView key={camera.id} camId={camera.id} src={`${import.meta.env.VITE_API_BASE_URL}/static/hls_output/${camera.id}/index.m3u8`}/>
                }
            )}
        </div>
    )
}