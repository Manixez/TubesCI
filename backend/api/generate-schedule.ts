import { Request, Response } from "express";

import { runGa } from "../services/gaService";
import { saveSchedule } from "../services/scheduleService";
import { ScheduleResult } from "../types/schedule";
import { computeCapacityWarning, parseScheduleInput } from "../validators/scheduleValidator";

export const generateSchedule = async (req: Request, res: Response): Promise<void> => {
    const { input, errors } = parseScheduleInput(req.body);
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

        const id = await saveSchedule(input, finalResult);
        res.json({ id, result: finalResult });
    } catch (err) {
        res.status(500).json({ error: "Gagal generate jadwal.", detail: String(err) });
    }
};
