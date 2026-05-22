import type { VercelRequest, VercelResponse } from "@vercel/node";

const resolveOrigin = (): string => {
    const raw = process.env.CORS_ORIGIN;
    if (!raw) {
        return "*";
    }
    return raw
        .split(",")
        .map((item) => item.trim())
        .filter((item) => item.length > 0)[0] || "*";
};

export const setCors = (res: VercelResponse): void => {
    res.setHeader("Access-Control-Allow-Origin", resolveOrigin());
    res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
};

export const handleOptions = (req: VercelRequest, res: VercelResponse): boolean => {
    if (req.method === "OPTIONS") {
        setCors(res);
        res.status(204).end();
        return true;
    }
    return false;
};

export const parseJsonBody = (req: VercelRequest): unknown => {
    if (!req.body) {
        return {};
    }
    if (typeof req.body === "string") {
        try {
            return JSON.parse(req.body);
        } catch {
            return {};
        }
    }
    return req.body;
};
