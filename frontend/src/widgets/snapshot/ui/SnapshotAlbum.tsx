import {SnapshotCard} from "@/entities/snapshot";
import type {Snapshot} from "@/entities/snapshot/api/types.ts";
import {useSnapshotAlbum} from "@/widgets/snapshot/model/useSnapshotAlbum.ts";
import {mediaUrl} from "@shared/api/media.ts";

export const SnapshotAlbum = () => {

    const {snapshots, loading, selectedImage, setSelectedImage} = useSnapshotAlbum();

    if (loading) {
        return <div>로딩중입니다..</div>
    }

    const sortedSnapshots = [...snapshots].sort((a, b) =>
        b.id - a.id
    );

    const groupedLogs = sortedSnapshots.reduce((acc, snapshot) => {
        const date:string = snapshot.timestamp.split('T')[0];
        if (!acc[date]) acc[date] = [];
        acc[date].push(snapshot);
        return acc;
    }, {} as Record<string, Snapshot[]>);

    return (
        <div className={"relative"}>
            <div className="max-w-full mx-auto p-6 space-y-12">
                {Object.entries(groupedLogs).map(([date, dateLogs]) => (
                    <section key={date} className="space-y-4">
                        {/* 날짜 헤더 */}
                        <div className="flex items-center gap-4">
                            <h2 className="text-2xl font-black text-gray-800">{date}</h2>
                            <div className="h-0.5 flex-1 bg-gray-100"></div>
                            <span className="text-sm font-bold text-gray-400">{dateLogs.length} photos</span>
                        </div>

                        {/* 그리드 레이아웃 */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
                            {dateLogs.map((snapshot) => (
                                <div
                                    key={snapshot.id}
                                    onClick={() => setSelectedImage(snapshot.image_path)} // 2. 클릭 시 경로 저장
                                    className="cursor-pointer hover:opacity-90 transition"
                                >
                                    <SnapshotCard snapshot={snapshot} />
                                </div>
                            ))}
                        </div>
                    </section>
                ))}
            </div>
            {/* 전체화면 모달 (Lightbox) */}
            {selectedImage && (
                <div
                    className="fixed inset-0 z-100 bg-black/95 flex items-center justify-center p-4 backdrop-blur-md"
                    onClick={() => setSelectedImage(null)} // 배경 클릭 시 닫기
                >
                    <div className="relative w-full h-full flex items-center justify-center">
                        {/* 닫기 버튼 */}
                        <button
                            className="absolute top-0 right-0 m-4 text-white text-5xl font-thin hover:text-gray-400 transition-colors z-110"
                            onClick={() => setSelectedImage(null)}
                        >
                            &times;
                        </button>

                        {/* 메인 이미지 */}
                        <img
                            src={mediaUrl(selectedImage)}
                            className="max-w-full max-h-full object-contain shadow-2xl animate-in zoom-in-95 duration-300"
                            alt="Full Screen"
                            onClick={(e) => e.stopPropagation()} // 이미지 클릭 시 닫히지 않게 보호
                        />
                    </div>
                </div>
            )}
        </div>
    );
}