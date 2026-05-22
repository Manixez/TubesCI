"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.runGa = void 0;
const child_process_1 = require("child_process");
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const resolveGaEntry = () => {
    const envEntry = process.env.GA_ENTRY;
    const candidates = [
        envEntry,
        path_1.default.resolve(process.cwd(), "ga_engine", "main.py"),
        path_1.default.resolve(process.cwd(), "..", "ga_engine", "main.py"),
    ].filter(Boolean);
    for (const candidate of candidates) {
        if (fs_1.default.existsSync(candidate)) {
            return candidate;
        }
    }
    throw new Error("GA entry script tidak ditemukan. Set GA_ENTRY jika perlu.");
};
const callGaApi = async (input, baseUrl) => {
    const response = await fetch(`${baseUrl.replace(/\/$/, "")}/generate`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(input),
    });
    if (!response.ok) {
        const text = await response.text();
        throw new Error(text || "GA API gagal dijalankan.");
    }
    return (await response.json());
};
const runGa = async (input) => {
    const gaApiUrl = process.env.GA_API_URL;
    if (gaApiUrl) {
        return callGaApi(input, gaApiUrl);
    }
    const python = process.env.GA_PYTHON || "python3";
    const entry = resolveGaEntry();
    return new Promise((resolve, reject) => {
        const child = (0, child_process_1.spawn)(python, [entry], {
            stdio: ["pipe", "pipe", "pipe"],
        });
        let stdout = "";
        let stderr = "";
        child.stdout.on("data", (chunk) => {
            stdout += chunk.toString();
        });
        child.stderr.on("data", (chunk) => {
            stderr += chunk.toString();
        });
        child.on("error", (err) => {
            reject(err);
        });
        child.on("close", (code) => {
            if (code !== 0) {
                reject(new Error(stderr || "GA engine gagal dijalankan."));
                return;
            }
            try {
                const parsed = JSON.parse(stdout);
                resolve(parsed);
            }
            catch (err) {
                reject(new Error("Output GA tidak valid."));
            }
        });
        child.stdin.write(JSON.stringify(input));
        child.stdin.end();
    });
};
exports.runGa = runGa;
