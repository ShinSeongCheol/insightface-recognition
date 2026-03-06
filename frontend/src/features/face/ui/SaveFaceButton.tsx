import {useSaveFace} from "../model/useSaveFace";
import type {Face} from "@/entities/face/api/types.ts";
import type {Dispatch, SetStateAction} from "react";

interface Props {
    faceId:number,
    newName:string,
    setIsEditing: Dispatch<SetStateAction<boolean>>,
    setFace:Dispatch<SetStateAction<Partial<Face | null>>>,
}

export const SaveFaceButton = ({faceId, newName, setIsEditing, setFace}:Props) => {

    const {handleSave} = useSaveFace(faceId, newName, setIsEditing, setFace)

    return (
        <button
            onClick={handleSave}
            className="w-full sm:flex-1 bg-blue-600 text-white py-3 sm:py-4 rounded-2xl font-bold shadow-lg hover:bg-blue-700 transition hover:cursor-pointer"
        >
            저장하기
        </button>
    )
}