import type { VercelRequest, VercelResponse } from "@vercel/node";

import { handleOptions, setCors } from "./_utils/http";

export default function handler(req: VercelRequest, res: VercelResponse): void {
    if (handleOptions(req, res)) {
        return;
    }

    setCors(res);
    res.status(200).json({ status: "ok" });
}
