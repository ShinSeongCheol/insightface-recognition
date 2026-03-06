import {mediaUrl} from "@shared/api/media.ts";
import type {Face} from "@/entities/face/api/types.ts";
import type {ReactNode} from "react";

interface Props {
    face: Face,
    action?: ReactNode
}

export const FaceCard = ({face, action}: Props) => {
    return (
        <div key={face.id} className="bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 group">

            {/* 이미지 섹션 */}
            <div className="relative aspect-square overflow-hidden bg-gray-100">
                <img
                    src={mediaUrl(face.image_path)}
                    alt={face.name}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                    onError={(e) => {
                        const target = e.currentTarget as HTMLImageElement
                        target.src = "https://via.placeholder.com/400?text=No+Image";
                    }}
                />
                <div className="absolute top-3 right-3 bg-white/80 backdrop-blur-md px-3 py-1 rounded-full text-xs font-bold text-gray-700 shadow-sm">
                    ID: {face.id}
                </div>
            </div>

            {/* 이름 및 정보 섹션 */}
            <div className="p-6">
                <h3 className="text-xl font-bold text-gray-800 mb-1">{face.name}</h3>
                <p className="text-sm text-gray-400">
                    {new Date(face.created_at).toLocaleDateString()} 등록됨
                </p>

                {action}
            </div>
        </div>
    )
}