export type ScheduleInput = {
    buildings: string[];
    guards: string[];
    shifts: string[];
    guardsPerShift: number;
    periodDays: number;
    minDaysOff?: number;
};

export type ScheduleRow = {
    day: string;
    building: string;
    shift: string;
    guards: string[];
};

export type GuardSummary = {
    name: string;
    totalShifts: number;
    buildings: string[];
    label: string;
    dailyAssignments: {
        day: string;
        shifts: {
            shift: string;
            building: string;
        }[];
    }[];
};

export type ScheduleMetrics = {
    missingGuards: number;
    doubleShiftDays: number;
    overlapShiftAssignments: number;
    dayOffShortage: number;
    workloadStdev: number;
    buildingRepeatExcess: number;
    totalPenalty: number;
};

export type ScheduleResult = {
    schedule: ScheduleRow[];
    guardSummary: GuardSummary[];
    warnings: string[];
    fitnessScore: number;
    metrics: ScheduleMetrics;
};

export type GenerateScheduleResponse = {
    id: string;
    result: ScheduleResult;
};

export type StoredSchedule = {
    id: string;
    input: ScheduleInput;
    result: ScheduleResult;
    createdAt: string;
};
