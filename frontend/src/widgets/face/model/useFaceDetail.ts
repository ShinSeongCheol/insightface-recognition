import {fetchFace} from "@features/face/api/fetchFaceApi.ts";
import {type ChangeEvent, useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import type {Face} from "@/entities/face/api/types.ts";

export const useFaceDetail = () => {
    const { id } = useParams();
    const [face, setFace] = useState<Partial<Face> | null>(null);
    const [isEditing, setIsEditing] = useState(false);
    const [newName, setNewName] = useState("");

    // 1. 상세 정보 불러오기
    useEffect(() => {
        let cancelled = false;

        if (!id) {
            return;
        }

        const load = async () => {
            try {
                const data = await fetchFace(id);

                if (!cancelled) {
                    setFace(data);
                    setNewName(data.name)
                }
            } catch (error){
                console.error(error);
            }
        }

        void load();

        return () => {
            cancelled = true;
        }

    }, [id]);

    const onChangeNewName = (e:ChangeEvent<HTMLInputElement>) => {
        setNewName(e.currentTarget.value)
    }

    return {face, newName, isEditing, setIsEditing, setFace, onChangeNewName};
}