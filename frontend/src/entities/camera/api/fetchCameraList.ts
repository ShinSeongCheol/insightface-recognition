import {httpClient} from "@shared/api/httpClient.ts";

export const fetchCameraList = async () => {
    const res = await httpClient.get('/cameras')
    return res.data
}