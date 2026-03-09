import { CameraView } from "@/entities/camera";

const Dashboard = () => {
    return (
        <div className="flex items-center justify-center min-h-screen w-full p-4">
            <div className={'grid grid-cols-1 lg:grid-cols-2 gap-2'}>
                <CameraView camId={1} src={`${import.meta.env.VITE_API_BASE_URL}/static/hls_output/1/index.m3u8`}/>
                <CameraView camId={2} src={`${import.meta.env.VITE_API_BASE_URL}/static/hls_output/1/index.m3u8`}/>
                <CameraView camId={3} src={`${import.meta.env.VITE_API_BASE_URL}/static/hls_output/1/index.m3u8`}/>
                <CameraView camId={4} src={`${import.meta.env.VITE_API_BASE_URL}/static/hls_output/1/index.m3u8`}/>
            </div>
        </div>
    );
};

export default Dashboard;