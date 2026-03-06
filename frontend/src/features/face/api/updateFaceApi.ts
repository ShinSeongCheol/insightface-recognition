import type {updateFaceRequest} from "@features/face/api/types.ts";
import {httpClient} from "@shared/api/httpClient.ts";
import type {Face} from "@/entities/face/api/types.ts";

export const updateFace = async (faceId: number, data: updateFaceRequest): Promise<Face> => {
    const res = await httpClient.patch(`/faces/${faceId}`, data)
    return res.data
}