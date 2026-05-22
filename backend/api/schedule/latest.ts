import type { VercelRequest, VercelResponse } from "@vercel/node";

import { getLatestSchedule, initDb } from "../../services/scheduleService";
import { handleOptions, setCors } from "../_utils/http";

export default async function handler(req: VercelRequest, res: VercelResponse): Promise<void> {
    if (handleOptions(req, res)) {
        return;
    }

    setCors(res);

    if (req.method !== "GET") {
        res.status(405).json({ error: "Method tidak diizinkan." });
        return;
    }

    try {
        await initDb();
        const schedule = await getLatestSchedule();
        if (!schedule) {
            res.status(404).json({ error: "Belum ada jadwal tersimpan." });
            return;
        }
        res.status(200).json(schedule);
    } catch (err) {
        res.status(500).json({ error: "Gagal mengambil jadwal.", detail: String(err) });
    }
}
