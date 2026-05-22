"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = handler;
const scheduleService_1 = require("../../services/scheduleService");
const http_1 = require("../_utils/http");
async function handler(req, res) {
    if ((0, http_1.handleOptions)(req, res)) {
        return;
    }
    (0, http_1.setCors)(res);
    if (req.method !== "GET") {
        res.status(405).json({ error: "Method tidak diizinkan." });
        return;
    }
    try {
        await (0, scheduleService_1.initDb)();
        const schedule = await (0, scheduleService_1.getLatestSchedule)();
        if (!schedule) {
            res.status(404).json({ error: "Belum ada jadwal tersimpan." });
            return;
        }
        res.status(200).json(schedule);
    }
    catch (err) {
        res.status(500).json({ error: "Gagal mengambil jadwal.", detail: String(err) });
    }
}
