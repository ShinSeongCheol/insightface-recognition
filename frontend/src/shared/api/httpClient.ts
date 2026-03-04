import {API_BASE_URL} from "./config.ts";
import axios from "axios";

export const httpClient = axios.create({
    baseURL: API_BASE_URL + "/api/v1",
    timeout: 10000,
    headers: {
        "Content-Type": "application/json"
    }
});