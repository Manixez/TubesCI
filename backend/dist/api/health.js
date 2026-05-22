"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = handler;
const http_1 = require("./_utils/http");
function handler(req, res) {
    if ((0, http_1.handleOptions)(req, res)) {
        return;
    }
    (0, http_1.setCors)(res);
    res.status(200).json({ status: "ok" });
}
