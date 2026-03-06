import {deleteFace} from "@features/face/api/deleteFaceApi.ts";
import {useNavigate} from "react-router-dom";

export const useDeleteFace = (faceId: number) => {
    const navigate = useNavigate();

    const handleDelete = async () => {
        if (!faceId) {
            return;
        }

        if (!window.confirm("정말로 삭제하시겠습니까? 관련 이미지 파일도 사라집니다.")) return;

        try {
            await deleteFace(faceId);
            alert("삭제 되었습니다.");
            navigate('/'); // 홈으로 이동
        } catch (error) {
            console.error(error)
            alert("삭제 중 오류가 발생했습니다.");
        }
    };

    return {handleDelete}
}