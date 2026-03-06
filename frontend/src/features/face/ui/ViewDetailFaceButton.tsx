import {useNavigate} from "react-router-dom";

export const ViewDetailFaceButton = ({faceId}: {faceId: number}) => {
    const navigate = useNavigate();

    return (
        <button
            className="w-full mt-5 py-3 bg-blue-50 text-blue-600 font-bold rounded-2xl hover:bg-blue-600 hover:text-white transition-colors duration-200 hover:cursor-pointer" onClick={() => navigate(`/faces/${faceId}`)}>
            상세 정보
        </button>
    )
}

export default ViewDetailFaceButton