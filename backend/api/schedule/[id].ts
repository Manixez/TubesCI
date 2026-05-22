import type { VercelRequest, VercelResponse } from "@vercel/node";

import { getSchedule, initDb } from "../../services/scheduleService";
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

    const id = Array.isArray(req.query.id) ? req.query.id[0] : req.query.id;
    if (!id) {
        res.status(400).json({ error: "ID wajib diisi." });
        return;
    }

    try {
        await initDb();
        const schedule = await getSchedule(String(id));
        if (!schedule) {
            res.status(404).json({ error: "Jadwal tidak ditemukan." });
            return;
        }
        res.status(200).json(schedule);
    } catch (err) {
        res.status(500).json({ error: "Gagal mengambil jadwal.", detail: String(err) });
    }
}
