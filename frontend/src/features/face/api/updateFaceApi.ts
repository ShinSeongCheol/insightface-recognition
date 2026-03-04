import type {Face, updateFaceRequest} from "@features/face/api/types.ts";
import {httpClient} from "@shared/api/httpClient.ts";

export const updateFace = async (faceId: string, data: updateFaceRequest): Promise<Face> => {
    const res = await httpClient.patch(`/faces/${faceId}`, data)
    return res.data
}