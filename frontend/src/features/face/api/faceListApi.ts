import type {FacesResponse} from "./types.ts";
import {httpClient} from "@shared/api/httpClient.ts";

export async function fetchFaces(): Promise<FacesResponse> {
    const res = await httpClient.get('/faces')
    return res.data
}