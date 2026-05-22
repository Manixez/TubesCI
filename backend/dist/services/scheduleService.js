"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getLatestSchedule = exports.getSchedule = exports.saveSchedule = exports.initDb = void 0;
const crypto_1 = __importDefault(require("crypto"));
const pg_1 = require("pg");
let pool = null;
const getPool = () => {
    if (!pool) {
        const connectionString = process.env.DATABASE_URL || process.env.PG_CONNECTION_STRING;
        if (!connectionString) {
            throw new Error("DATABASE_URL atau PG_CONNECTION_STRING wajib diisi.");
        }
        pool = new pg_1.Pool({ connectionString });
    }
    return pool;
};
const initDb = async () => {
    const db = getPool();
    await db.query("CREATE TABLE IF NOT EXISTS schedules (id uuid PRIMARY KEY, created_at timestamptz DEFAULT now(), input jsonb NOT NULL, result jsonb NOT NULL)");
};
exports.initDb = initDb;
const saveSchedule = async (input, result) => {
    const db = getPool();
    const id = crypto_1.default.randomUUID();
    await db.query("INSERT INTO schedules (id, input, result) VALUES ($1, $2, $3)", [
        id,
        input,
        result,
    ]);
    return id;
};
exports.saveSchedule = saveSchedule;
const getSchedule = async (id) => {
    const db = getPool();
    const result = await db.query("SELECT id, input, result, created_at FROM schedules WHERE id = $1", [id]);
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
exports.getSchedule = getSchedule;
const getLatestSchedule = async () => {
    const db = getPool();
    const result = await db.query("SELECT id, input, result, created_at FROM schedules ORDER BY created_at DESC LIMIT 1");
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
exports.getLatestSchedule = getLatestSchedule;
