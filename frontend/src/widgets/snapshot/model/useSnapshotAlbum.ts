import {useEffect, useState} from "react";
import type {Snapshot} from "@/entities/snapshot/api/types.ts";
import {fetchSnapshotList} from "@/entities/snapshot";

export const useSnapshotAlbum = () => {
    const [snapshots, setSnapshots] = useState<Snapshot[]>([])

    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let ignore = false;


        async function fetchData() {
            try {
                setLoading(true);

                const res = await fetchSnapshotList();
                if (!ignore) {
                    setSnapshots(res.snapshots)
                }

            } catch (error) {
                console.error('snapshots fetch 실패:', error);
            } finally {
                setLoading(false);
            }
        }

        fetchData().then();

        return () => {
            ignore = true;
        }

    }, []);

    return {snapshots, loading}
}