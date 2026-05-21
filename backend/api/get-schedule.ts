import { Request, Response } from "express";

import { getLatestSchedule, getSchedule } from "../services/scheduleService";

export const getScheduleHandler = async (req: Request, res: Response): Promise<void> => {
    try {
        const schedule = await getSchedule(req.params.id);
        if (!schedule) {
            res.status(404).json({ error: "Jadwal tidak ditemukan." });
            return;
        }
        res.json(schedule);
    } catch (err) {
        res.status(500).json({ error: "Gagal mengambil jadwal.", detail: String(err) });
    }
};

export const getLatestScheduleHandler = async (
    _req: Request,
    res: Response
): Promise<void> => {
    try {
        const schedule = await getLatestSchedule();
        if (!schedule) {
            res.status(404).json({ error: "Belum ada jadwal tersimpan." });
            return;
        }
        res.json(schedule);
    } catch (err) {
        res.status(500).json({ error: "Gagal mengambil jadwal.", detail: String(err) });
    }
};
