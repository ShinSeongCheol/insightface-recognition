import {httpClient} from "@shared/api/httpClient.ts";
import type {Camera} from "@/entities/camera";

type CreateCameraRequest = Omit<Camera, 'id' | 'is_active'>

export const postCamera = async  (data: CreateCameraRequest): Promise<Camera> => {
    const res = await httpClient.post('/cameras', data, {headers: {'Content-Type': "application/json"}})
    return res.data
}