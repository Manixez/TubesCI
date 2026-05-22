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
    if (req.method !== "POST") {
        res.status(405).json({ error: "Method tidak diizinkan." });
        return;
    }
    const body = (0, http_1.parseJsonBody)(req);
    if (!body?.input || !body?.result) {
        res.status(400).json({ error: "Input dan result wajib diisi." });
        return;
    }
    try {
        await (0, scheduleService_1.initDb)();
        const id = await (0, scheduleService_1.saveSchedule)(body.input, body.result);
        res.status(200).json({ id });
    }
    catch (err) {
        res.status(500).json({ error: "Gagal menyimpan jadwal.", detail: String(err) });
    }
}
