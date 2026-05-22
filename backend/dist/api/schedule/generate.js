"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = handler;
const gaService_1 = require("../../services/gaService");
const scheduleService_1 = require("../../services/scheduleService");
const scheduleValidator_1 = require("../../validators/scheduleValidator");
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
    const payload = (0, http_1.parseJsonBody)(req);
    const { input, errors } = (0, scheduleValidator_1.parseScheduleInput)(payload);
    if (errors.length > 0) {
        res.status(400).json({ errors });
        return;
    }
    try {
        const warning = (0, scheduleValidator_1.computeCapacityWarning)(input);
        const gaResult = await (0, gaService_1.runGa)(input);
        const warnings = Array.from(new Set([...(warning ? [warning] : []), ...(gaResult.warnings || [])]));
        const finalResult = {
            ...gaResult,
            warnings,
        };
        await (0, scheduleService_1.initDb)();
        const id = await (0, scheduleService_1.saveSchedule)(input, finalResult);
        res.status(200).json({ id, result: finalResult });
    }
    catch (err) {
        res.status(500).json({ error: "Gagal generate jadwal.", detail: String(err) });
    }
}
