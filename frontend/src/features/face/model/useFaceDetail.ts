import type {Face} from "@features/face/api/types.ts";
import {fetchFace} from "@features/face/api/fetchFaceApi.ts";
import {useEffect, useState} from "react";
import {useNavigate, useParams} from "react-router-dom";
import {updateFace} from "@features/face/api/updateFaceApi.ts";
import {deleteFace} from "@features/face/api/deleteFaceApi.ts";

export const useFaceDetail = () => {
    const navigate = useNavigate();

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

    // 2. 삭제 핸들러
    const handleDelete = async () => {
        if (!id) {
            return;
        }

        if (!window.confirm("정말로 삭제하시겠습니까? 관련 이미지 파일도 사라집니다.")) return;

        try {
            await deleteFace(id);
            alert("삭제 되었습니다.");
            navigate('/'); // 홈으로 이동
        } catch (error) {
            console.error(error)
            alert("삭제 중 오류가 발생했습니다.");
        }
    };

    // 3. 수정(이름 변경) 핸들러
    const handleUpdate = async () => {
        if (!id) {
            return;
        }

        try {
            await updateFace(id, {name: newName})

            setFace({ ...face, name: newName });

            setIsEditing(false);
            alert("이름이 변경되었습니다.");
        } catch (error) {
            console.error(error)
            alert("수정 중 오류가 발생했습니다.");
        }
    };

    const toggleEditing = (toggle:boolean) => {
        setIsEditing(toggle)
    }

    return {face, newName, isEditing, toggleEditing, setNewName, handleUpdate, handleDelete};
}