import {API_BASE_URL} from "./config.ts";

export const mediaUrl = (path: string) => {
    return `${API_BASE_URL}/${path}`;
}