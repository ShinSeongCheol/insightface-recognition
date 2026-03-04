import type {CreateFaceRequest, Face} from "./types.ts";
import {httpClient} from "@shared/api/httpClient.ts";

export async function registerFace(data:CreateFaceRequest): Promise<Face> {
    const formData = new FormData();
    formData.append('name', data.name);
    formData.append('file', data.file);

    const res = await httpClient.post('/faces', formData, {headers: {'Content-Type': "multipart/form-data"}})
    return res.data
}