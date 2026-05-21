export interface ScheduleInput {
    buildings: string[];
    guards: string[];
    shifts: string[];
    guardsPerShift: number;
    periodDays: number;
    minDaysOff?: number;
}

export interface ScheduleRow {
    day: string;
    building: string;
    shift: string;
    guards: string[];
}

export interface GuardSummary {
    name: string;
    totalShifts: number;
    buildings: string[];
    label: string;
}

export interface ScheduleMetrics {
    missingGuards: number;
    doubleShiftDays: number;
    dayOffShortage: number;
    workloadStdev: number;
    buildingRepeatExcess: number;
    totalPenalty: number;
}

export interface ScheduleResult {
    schedule: ScheduleRow[];
    guardSummary: GuardSummary[];
    warnings: string[];
    fitnessScore: number;
    metrics: ScheduleMetrics;
}

export interface StoredSchedule {
    id: string;
    input: ScheduleInput;
    result: ScheduleResult;
    createdAt: string;
}
