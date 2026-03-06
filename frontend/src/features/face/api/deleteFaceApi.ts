import {httpClient} from "@shared/api/httpClient.ts";

export const deleteFace = async (faceId: number) => {
    const res = await httpClient.delete(`/faces/${faceId}`)
    return res.data
}