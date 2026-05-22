import { spawn } from "child_process";
import fs from "fs";
import path from "path";

import { ScheduleInput, ScheduleResult } from "../types/schedule";

const resolveGaEntry = (): string => {
    const envEntry = process.env.GA_ENTRY;
    const candidates = [
        envEntry,
        path.resolve(process.cwd(), "ga_engine", "main.py"),
        path.resolve(process.cwd(), "..", "ga_engine", "main.py"),
    ].filter(Boolean) as string[];

    for (const candidate of candidates) {
        if (fs.existsSync(candidate)) {
            return candidate;
        }
    }

    throw new Error("GA entry script tidak ditemukan. Set GA_ENTRY jika perlu.");
};

const normalizeBaseUrl = (rawUrl: string): string => {
    const trimmed = rawUrl.trim();
    if (trimmed.length === 0) {
        return "";
    }

    const firstToken = trimmed.split(/\s+/)[0];
    const unquoted = firstToken.replace(/^("|')|("|')$/g, "");

    if (!/^https?:\/\//i.test(unquoted)) {
        return `https://${unquoted}`;
    }
    return unquoted;
};

const sanitizeBaseUrl = (rawUrl: string): string => rawUrl.replace(/[^\x20-\x7E]/g, "");

const ensureValidBaseUrl = (rawUrl: string): string => {
    const normalized = normalizeBaseUrl(rawUrl);
    if (!normalized) {
        throw new Error("GA_API_URL kosong.");
    }

    const cleaned = sanitizeBaseUrl(normalized);
    try {
        return new URL(cleaned).toString().replace(/\/$/, "");
    } catch {
        throw new Error(`GA_API_URL tidak valid: ${JSON.stringify(cleaned)}`);
    }
};

const callGaApi = async (input: ScheduleInput, baseUrl: string): Promise<ScheduleResult> => {
    const normalized = ensureValidBaseUrl(baseUrl);
    const response = await fetch(`${normalized}/generate`, {
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

    return (await response.json()) as ScheduleResult;
};

export const runGa = async (input: ScheduleInput): Promise<ScheduleResult> => {
    const gaApiUrl = process.env.GA_API_URL?.trim();
    if (gaApiUrl) {
        return callGaApi(input, gaApiUrl);
    }

    const python = process.env.GA_PYTHON || "python3";
    const entry = resolveGaEntry();

    return new Promise((resolve, reject) => {
        const child = spawn(python, [entry], {
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
                const parsed = JSON.parse(stdout) as ScheduleResult;
                resolve(parsed);
            } catch (err) {
                reject(new Error("Output GA tidak valid."));
            }
        });

        child.stdin.write(JSON.stringify(input));
        child.stdin.end();
    });
};
