import {updateFace} from "@features/face/api/updateFaceApi.ts";
import type {Dispatch, SetStateAction} from "react";
import type {Face} from "@/entities/face/api/types.ts";

export const useSaveFace = (id: number, newName: string, setIsEditing: Dispatch<SetStateAction<boolean>>, setFace: Dispatch<SetStateAction<Partial<Face | null>>>) => {

    const handleSave = async () => {
        if (!id) {
            return;
        }

        try {
            await updateFace(id, {name: newName})

            alert("이름이 변경되었습니다.");
            setFace(prev => ({
                ...prev,
                name: newName
            }));
            setIsEditing(false)

        } catch (error) {
            console.error(error)
            alert("수정 중 오류가 발생했습니다.");
        }
    }

    return {handleSave}
}