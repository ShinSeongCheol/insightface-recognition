import {httpClient} from "@shared/api/httpClient.ts";

export const deleteFace = async (faceId: string) => {
    const res = await httpClient.delete(`/faces/${faceId}`)
    return res.data
}