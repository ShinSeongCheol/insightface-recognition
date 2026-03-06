import {httpClient} from "@shared/api/httpClient.ts";
import type {Snapshot} from "./types.ts";

export const fetchSnapshotList = async (): Promise<{"snapshots": Snapshot[]}> => {
    const res = await httpClient.get('/snapshots')
    return res.data
}