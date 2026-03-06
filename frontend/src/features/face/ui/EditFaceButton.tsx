import * as React from "react";

export const EditFaceButton = ({setIsEditing}:{setIsEditing: React.Dispatch<React.SetStateAction<boolean>>}) => {
    return (
        <button
            onClick={() => {setIsEditing(true)}}
            className="w-full sm:flex-1 bg-blue-600 text-white py-3 sm:py-4 rounded-2xl font-bold shadow-lg hover:bg-blue-500 transition  hover:cursor-pointer"
        >
            정보 수정
        </button>
    )
}