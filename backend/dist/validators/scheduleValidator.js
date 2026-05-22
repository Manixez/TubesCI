"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.computeCapacityWarning = exports.parseScheduleInput = void 0;
const DEFAULT_SHIFTS = ["Shift 1", "Shift 2"];
const toStringArray = (value) => {
    if (!Array.isArray(value)) {
        return [];
    }
    return value
        .map((item) => String(item).trim())
        .filter((item) => item.length > 0);
};
const toNumber = (value, fallback) => {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
};
const parseScheduleInput = (payload) => {
    if (!payload || typeof payload !== "object") {
        return {
            input: {
                buildings: [],
                guards: [],
                shifts: DEFAULT_SHIFTS,
                guardsPerShift: 1,
                periodDays: 7,
                minDaysOff: 0,
            },
            errors: ["Payload tidak valid."],
        };
    }
    const data = payload;
    const buildings = toStringArray(data.buildings);
    const guards = toStringArray(data.guards);
    const shiftsPayload = toStringArray(data.shifts);
    const shifts = shiftsPayload.length > 0 ? shiftsPayload : DEFAULT_SHIFTS;
    const periodDays = toNumber(data.periodDays ?? data.period_days, 7);
    const guardsPerShift = toNumber(data.guardsPerShift ?? data.guards_per_shift, 1);
    const minDaysOff = toNumber(data.minDaysOff ?? data.min_days_off, 0);
    const errors = [];
    if (buildings.length === 0) {
        errors.push("Daftar gedung tidak boleh kosong.");
    }
    if (guards.length === 0) {
        errors.push("Daftar satpam tidak boleh kosong.");
    }
    if (guardsPerShift <= 0) {
        errors.push("Satpam per shift harus > 0.");
    }
    if (periodDays <= 0) {
        errors.push("Jumlah hari harus > 0.");
    }
    if (minDaysOff < 0) {
        errors.push("Hari libur minimum tidak boleh negatif.");
    }
    if (minDaysOff > periodDays) {
        errors.push("Hari libur minimum tidak boleh melebihi jumlah hari.");
    }
    return {
        input: {
            buildings,
            guards,
            shifts,
            guardsPerShift,
            periodDays,
            minDaysOff,
        },
        errors,
    };
};
exports.parseScheduleInput = parseScheduleInput;
const computeCapacityWarning = (input) => {
    const minDaysOff = input.minDaysOff ?? 0;
    const totalRequired = input.periodDays * input.shifts.length * input.buildings.length * input.guardsPerShift;
    const maxPerGuard = input.periodDays - minDaysOff;
    const maxCapacity = maxPerGuard * input.guards.length;
    if (maxCapacity < totalRequired) {
        return ("Jumlah satpam tidak mencukupi untuk memenuhi seluruh shift secara adil. " +
            "Tambah satpam atau kurangi gedung/shift/hari libur.");
    }
    return null;
};
exports.computeCapacityWarning = computeCapacityWarning;
