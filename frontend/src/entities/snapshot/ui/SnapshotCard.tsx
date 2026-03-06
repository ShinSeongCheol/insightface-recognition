import {mediaUrl} from "@shared/api/media.ts";
import type {Snapshot} from "@/entities/snapshot/api/types.ts";

export const SnapshotCard = ({snapshot}: {snapshot: Snapshot}) => {
    return (
        <div className="group relative overflow-hidden rounded-2xl bg-gray-100 aspect-square cursor-pointer transition-all hover:ring-4 hover:ring-blue-500">
            <img
                src={mediaUrl(snapshot.image_path)}
                alt="captured"
                className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
            />
            {/* 하단 오버레이 (시간 표시) */}
            <div className="absolute bottom-0 left-0 right-0 bg-linear-to-t from-black/70 to-transparent p-3 opacity-0 group-hover:opacity-100 transition-opacity">
                <p className="text-white text-xs font-medium">
                    ⏱ {new Date(snapshot.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </p>
            </div>
        </div>
    )
}