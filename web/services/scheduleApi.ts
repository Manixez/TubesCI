import { GenerateScheduleResponse, ScheduleInput, StoredSchedule } from "../types/schedule";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:4000";

const handleResponse = async <T>(response: Response): Promise<T> => {
    if (!response.ok) {
        const text = await response.text();
        throw new Error(text || "Request gagal.");
    }
    return (await response.json()) as T;
};

export const generateSchedule = async (
    input: ScheduleInput
): Promise<GenerateScheduleResponse> => {
    const response = await fetch(`${API_BASE}/api/schedule/generate`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(input),
    });

    return handleResponse<GenerateScheduleResponse>(response);
};

export const getLatestSchedule = async (): Promise<StoredSchedule | null> => {
    const response = await fetch(`${API_BASE}/api/schedule/latest`, {
        method: "GET",
    });

    if (response.status === 404) {
        return null;
    }

    return handleResponse<StoredSchedule>(response);
};
