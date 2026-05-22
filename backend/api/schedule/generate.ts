import type { VercelRequest, VercelResponse } from "@vercel/node";

import { runGa } from "../../services/gaService";
import { initDb, saveSchedule } from "../../services/scheduleService";
import { ScheduleResult } from "../../types/schedule";
import { computeCapacityWarning, parseScheduleInput } from "../../validators/scheduleValidator";
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

    const payload = parseJsonBody(req);
    const { input, errors } = parseScheduleInput(payload);
    if (errors.length > 0) {
        res.status(400).json({ errors });
        return;
    }

    try {
        const warning = computeCapacityWarning(input);
        const gaResult = await runGa(input);
        const warnings = Array.from(
            new Set([...(warning ? [warning] : []), ...(gaResult.warnings || [])])
        );
        const finalResult: ScheduleResult = {
            ...gaResult,
            warnings,
        };

        await initDb();
        const id = await saveSchedule(input, finalResult);
        res.status(200).json({ id, result: finalResult });
    } catch (err) {
        res.status(500).json({ error: "Gagal generate jadwal.", detail: String(err) });
    }
}
