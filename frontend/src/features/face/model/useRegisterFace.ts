import axios from "axios";
import {useNavigate} from "react-router-dom";
import {type ChangeEvent, type SubmitEventHandler, useEffect, useState} from "react";
import type {CreateFaceRequest} from "@features/face/api/types.ts";
import {registerFace} from "@features/face/api/registerFaceApi.ts";

export const useRegisterFace = () => {
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [file, setFile] = useState<File|null>(null);
    const [preview, setPreview] = useState<string|null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);

    // 파일 선택 시 미리보기 생성
    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.currentTarget.files?.[0];
        if (selectedFile) {
            setFile(selectedFile);
            setPreview((prev) => {
                if (prev) URL.revokeObjectURL(prev);
                return URL.createObjectURL(selectedFile);
            });
        }
    };

    // 이름 변경 시
    const handleNameChange = (e:ChangeEvent<HTMLInputElement>) => {
        setName(e.currentTarget.value);
    }

    // 얼굴 등록
    const handleSubmit: SubmitEventHandler<HTMLFormElement> = async (e) => {
        e.preventDefault();

        if (!name || !file) {
            alert("이름과 사진을 모두 입력해주세요!");
            return;
        }

        setIsSubmitting(true);

        const requestData: CreateFaceRequest = {
            name: name,
            file: file,
        }

        try {
            const res = await registerFace(requestData);
            if (res) {
                alert("성공적으로 등록되었습니다!");
            }

            navigate('/'); // 등록 후 홈 화면으로 이동
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const errorMsg = error.response?.data?.detail ?? "등록 중 오류가 발생했습니다.";
                alert(errorMsg);
            } else if (error instanceof Error) {
                alert(error.message);
            } else {
                alert("알 수 없는 오류가 발생했습니다.");
            }
        } finally {
            setIsSubmitting(false);
        }
    };

    useEffect(() => {
        return () => {
            if (preview) URL.revokeObjectURL(preview);
        };
    }, [preview]);

    return {name, preview, isSubmitting, handleFileChange, handleNameChange, handleSubmit}
}