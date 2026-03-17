import {useEffect, useState} from "react";
import {type Camera, fetchCameraList} from "@/entities/camera";

export const useCameraGridViewWidget = () => {
    const [cameras, setCameras] = useState<Camera[]>([])
    const [isLoading, setIsLoading] = useState(true);

    const fetchCameras = async () => {
        try {
            const res = await fetchCameraList()
            setCameras(res.cameras);
        }catch (e) {
            console.error(e);
        }finally {
            setIsLoading(false)
        }
    }

    useEffect(() => {
        fetchCameras()
    }, []);

    return {cameras, isLoading}
}