import {useDeleteFace} from "../model/useDeleteFace.ts";

export const DeleteFaceButton = ({faceId}: {faceId:number}) => {

    const {handleDelete} = useDeleteFace(faceId);

    return (
        <button
            onClick={handleDelete}
            className="w-full sm:flex-1 bg-red-50 text-red-600 py-3 sm:py-4 rounded-2xl font-bold hover:bg-red-100 transition  hover:cursor-pointer"
        >
            삭제
        </button>
    )
}