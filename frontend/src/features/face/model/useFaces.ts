import {fetchFaces} from "../api/faceListApi.ts";
import {useEffect, useState} from "react";
import type {Face} from "../api/types.ts";

export function useFaces() {

    const [faces, setFaces] = useState<Face[]>([])
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let ignore = false;


        async function fetchData() {
            try {
                setLoading(true);

                const res = await fetchFaces();
                if (!ignore) {
                    setFaces(res.faces)
                }

            } catch (error) {
                console.error('faces fetch 실패:', error);
            } finally {
                setLoading(false);
            }
        }

        fetchData().then();

        return () => {
            ignore = true;
        }

    }, []);

    return {faces, loading};
}