import type { VercelRequest, VercelResponse } from "@vercel/node";

import { initDb, saveSchedule } from "../../services/scheduleService";
import { handleOptions, parseJsonBody, setCors } from "../_utils/http";

export default async function handler(req: VercelRequest, res: VercelResponse): Promise<void> {
    if (handleOptions(req, res)) {
        return;
    }

    setCors(res);

    if (req.method !== "POST") {
        res.status(405).json({ error: "Method tidak diizinkan." });
        return;
    }

    const body = parseJsonBody(req) as { input?: unknown; result?: unknown };
    if (!body?.input || !body?.result) {
        res.status(400).json({ error: "Input dan result wajib diisi." });
        return;
    }

    try {
        await initDb();
        const id = await saveSchedule(body.input as any, body.result as any);
        res.status(200).json({ id });
    } catch (err) {
        res.status(500).json({ error: "Gagal menyimpan jadwal.", detail: String(err) });
    }
}
