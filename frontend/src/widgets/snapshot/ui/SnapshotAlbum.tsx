import {SnapshotCard} from "@/entities/snapshot";
import type {Snapshot} from "@/entities/snapshot/api/types.ts";
import {useSnapshotAlbum} from "@/widgets/snapshot/model/useSnapshotAlbum.ts";

export const SnapshotAlbum = () => {

    const {snapshots, loading} = useSnapshotAlbum();

    if (loading) {
        return <div>로딩중입니다..</div>
    }

    const sortedSnapshots = [...snapshots].sort((a, b) =>
        new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );

    const groupedLogs = sortedSnapshots.reduce((acc, snapshot) => {
        const date:string = snapshot.timestamp.split('T')[0];
        if (!acc[date]) acc[date] = [];
        acc[date].push(snapshot);
        return acc;
    }, {} as Record<string, Snapshot[]>);

    return (
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
                            <SnapshotCard key={snapshot.id} snapshot={snapshot} />
                        ))}
                    </div>
                </section>
            ))}
        </div>
    );
}