import type {Dispatch, SetStateAction} from "react";

export const CancelFaceButton = ({setIsEditing}:{setIsEditing: Dispatch<SetStateAction<boolean>>}) => {
    return(
        <button
            onClick={() => setIsEditing(false)}
            className="w-full sm:flex-1 bg-gray-500 text-white py-3 sm:py-4 rounded-2xl font-bold hover:bg-gray-400 transition  hover:cursor-pointer"
        >
            취소
        </button>
    )
}