"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseJsonBody = exports.handleOptions = exports.setCors = void 0;
const resolveOrigin = () => {
    const raw = process.env.CORS_ORIGIN;
    if (!raw) {
        return "*";
    }
    return raw
        .split(",")
        .map((item) => item.trim())
        .filter((item) => item.length > 0)[0] || "*";
};
const setCors = (res) => {
    res.setHeader("Access-Control-Allow-Origin", resolveOrigin());
    res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
};
exports.setCors = setCors;
const handleOptions = (req, res) => {
    if (req.method === "OPTIONS") {
        (0, exports.setCors)(res);
        res.status(204).end();
        return true;
    }
    return false;
};
exports.handleOptions = handleOptions;
const parseJsonBody = (req) => {
    if (!req.body) {
        return {};
    }
    if (typeof req.body === "string") {
        try {
            return JSON.parse(req.body);
        }
        catch {
            return {};
        }
    }
    return req.body;
};
exports.parseJsonBody = parseJsonBody;
