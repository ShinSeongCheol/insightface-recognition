export type Face = {
    id: number,
    name: string,
    image_path: string,
    embedding: [],
    has_embedding: boolean,
    normalized_embedding: number,
    created_at: string,
    updated_at: string
}

export type FacesResponse = {
    faces: Face[],
    count: number;
}

export type CreateFaceRequest = {
    name: string,
    file: File,
}

export type updateFaceRequest = {
    name: string,
}