import {httpClient} from "@shared/api/httpClient.ts";
import type {Face} from "@/entities/face/api/types.ts";

export async function fetchFaceList(): Promise<{"faces": Face[]}> {
    const res = await httpClient.get('/faces')
    return res.data
}