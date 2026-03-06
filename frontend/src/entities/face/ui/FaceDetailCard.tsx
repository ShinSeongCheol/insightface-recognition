// 데이터만 보여주는 '멍청한' 컴포넌트
import {mediaUrl} from "@shared/api/media.ts";
import type {Face} from "../api/types";
import type {ChangeEvent, ReactNode} from "react";

interface Props {
    face: Face,
    newName: string,
    onChangeNewName: (e: ChangeEvent<HTMLInputElement>) => void,
    isEditing: boolean,
    saveButton: ReactNode,
    cancelButton: ReactNode,
    editButton: ReactNode,
    deleteButton: ReactNode
}

export const FaceDetailCard = ({ face, newName, onChangeNewName, isEditing, saveButton, cancelButton, editButton, deleteButton }: Props) => {
    return (
        <div className="bg-white rounded-3xl md:rounded-4xl shadow-2xl overflow-hidden flex flex-col md:flex-row border border-gray-100">
            {/* 이미지 섹션 */}
            <div className="w-full md:w-1/2 bg-gray-50">
                <img
                    src={mediaUrl(face.image_path)}
                    alt={face.name}
                    className="w-full h-64 sm:h-80 md:h-full object-cover"
                />
            </div>

            {/* 정보 및 버튼 섹션 */}
            <div className="w-full md:w-1/2 p-5 sm:p-6 md:p-12 flex flex-col">
                <div className="flex-1 flex flex-col justify-between items-start">
                    <div className="w-full">
                        <span className="inline-block bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-[11px] sm:text-xs font-bold uppercase">
                        Face ID: {face.id}
                        </span>

                        {isEditing ? (
                            <input
                                type="text"
                                className="block w-full text-2xl sm:text-3xl md:text-4xl font-black mt-4 sm:mt-6 p-2 border-b-4 border-blue-600 focus:outline-none"
                                value={newName}
                                onChange={onChangeNewName}
                                autoFocus
                            />
                        ) : (
                            <h1 className="text-3xl sm:text-4xl md:text-5xl font-black text-gray-900 mt-4 sm:mt-6 wrap-break-word">
                                {face.name}
                            </h1>
                        )}
                    </div>

                    <div className="mt-6 sm:mt-8 space-y-2 text-sm sm:text-base text-gray-500">
                        <p>📅 등록 일자: {face.created_at ? new Date(face.created_at).toLocaleString() : "-"}</p>
                    </div>
                </div>

                {/* 액션 버튼 */}
                <div className="mt-6 sm:mt-8 md:mt-12 flex flex-col sm:flex-row gap-3 sm:gap-4">
                    {isEditing ? saveButton:editButton}
                    {isEditing ? cancelButton:deleteButton}
                </div>
            </div>
        </div>
    );
}
