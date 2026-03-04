import {httpClient} from "@shared/api/httpClient.ts";
import type {Face} from "@features/face/api/types.ts";

export const fetchFace = async (faceId: string): Promise<Face> => {
    const res = await httpClient.get(`/faces/${faceId}`)
    return res.data
}