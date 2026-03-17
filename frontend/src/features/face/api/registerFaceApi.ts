import type {CreateFaceRequest} from "./types.ts";
import {httpClient} from "@shared/api/httpClient.ts";
import type {Face} from "@/entities/face/api/types.ts";

export async function registerFace(data:CreateFaceRequest): Promise<Face> {
    const formData = new FormData();
    formData.append('name', data.name);
    formData.append('file', data.file);

    const res = await httpClient.post('/faces', formData, {headers: {'Content-Type': "multipart/form-data"}})
    return res.data
}