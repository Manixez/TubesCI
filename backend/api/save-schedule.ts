import { Request, Response } from "express";

import { saveSchedule } from "../services/scheduleService";

export const saveScheduleHandler = async (req: Request, res: Response): Promise<void> => {
    const body = req.body as { input?: unknown; result?: unknown };
    if (!body?.input || !body?.result) {
        res.status(400).json({ error: "Input dan result wajib diisi." });
        return;
    }

    try {
        const id = await saveSchedule(body.input as any, body.result as any);
        res.json({ id });
    } catch (err) {
        res.status(500).json({ error: "Gagal menyimpan jadwal.", detail: String(err) });
    }
};
