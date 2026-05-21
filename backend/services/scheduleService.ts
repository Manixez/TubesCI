import crypto from "crypto";
import { Pool } from "pg";

import { ScheduleInput, ScheduleResult, StoredSchedule } from "../types/schedule";

let pool: Pool | null = null;

const getPool = (): Pool => {
    if (!pool) {
        const connectionString = process.env.DATABASE_URL || process.env.PG_CONNECTION_STRING;
        if (!connectionString) {
            throw new Error("DATABASE_URL atau PG_CONNECTION_STRING wajib diisi.");
        }
        pool = new Pool({ connectionString });
    }
    return pool;
};

export const initDb = async (): Promise<void> => {
    const db = getPool();
    await db.query(
        "CREATE TABLE IF NOT EXISTS schedules (id uuid PRIMARY KEY, created_at timestamptz DEFAULT now(), input jsonb NOT NULL, result jsonb NOT NULL)"
    );
};

export const saveSchedule = async (
    input: ScheduleInput,
    result: ScheduleResult
): Promise<string> => {
    const db = getPool();
    const id = crypto.randomUUID();
    await db.query("INSERT INTO schedules (id, input, result) VALUES ($1, $2, $3)", [
        id,
        input,
        result,
    ]);
    return id;
};

export const getSchedule = async (id: string): Promise<StoredSchedule | null> => {
    const db = getPool();
    const result = await db.query(
        "SELECT id, input, result, created_at FROM schedules WHERE id = $1",
        [id]
    );
    if (result.rows.length === 0) {
        return null;
    }
    const row = result.rows[0];
    return {
        id: row.id,
        input: row.input,
        result: row.result,
        createdAt: row.created_at,
    };
};

export const getLatestSchedule = async (): Promise<StoredSchedule | null> => {
    const db = getPool();
    const result = await db.query(
        "SELECT id, input, result, created_at FROM schedules ORDER BY created_at DESC LIMIT 1"
    );
    if (result.rows.length === 0) {
        return null;
    }
    const row = result.rows[0];
    return {
        id: row.id,
        input: row.input,
        result: row.result,
        createdAt: row.created_at,
    };
};
