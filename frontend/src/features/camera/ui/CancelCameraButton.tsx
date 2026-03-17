import {useNavigate} from "react-router-dom";

export const CancelCameraButton = () => {
    const navigate = useNavigate();

    return (
        <button type={'button'} className={'w-full py-2 rounded-2xl text-white text-xl shadow-lg transition-all bg-gray-500 hover:bg-gray-400 hover:cursor-pointer active:scale-[0.98]'} onClick={() => navigate(-1)}>
            취소
        </button>
    )
}