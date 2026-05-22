"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import BuildingInput from "../components/BuildingInput";
import GuardInput from "../components/GuardInput";
import ShiftInput from "../components/ShiftInput";
import GuardSummaryTable from "../components/GuardSummaryTable";
import ScheduleTable from "../components/ScheduleTable";
import { generateSchedule } from "../services/scheduleApi";
import { ScheduleInput, ScheduleResult } from "../types/schedule";

const parseNames = (raw: string, count: number, prefix: string): string[] => {
    const trimmed = raw
        .split(",")
        .map((name) => name.trim())
        .filter((name) => name.length > 0);

    const result = trimmed.slice(0, count);
    for (let idx = result.length; idx < count; idx += 1) {
        if (prefix === "S") {
            result.push(`S${String(idx + 1).padStart(2, "0")}`);
        } else {
            result.push(`${prefix} ${idx + 1}`);
        }
    }
    return result;
};

const parseShiftNames = (raw: string): string[] => {
    const shifts = raw
        .split(",")
        .map((name) => name.trim())
        .filter((name) => name.length > 0);
    return shifts.length > 0 ? shifts : ["Shift 1", "Shift 2"];
};

export default function HomePage() {
    const router = useRouter();

    const [buildingCount, setBuildingCount] = useState(3);
    const [buildingNames, setBuildingNames] = useState("Gedung A, Gedung B, Gedung C");
    const [guardCount, setGuardCount] = useState(12);
    const [guardNames, setGuardNames] = useState(
        "S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12"
    );
    const [shiftNames, setShiftNames] = useState("Shift 1, Shift 2");
    const [guardsPerShift, setGuardsPerShift] = useState(2);
    const [periodDays, setPeriodDays] = useState(7);
    const [minDaysOff, setMinDaysOff] = useState(2);

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<ScheduleResult | null>(null);

    const payload = useMemo<ScheduleInput>(
        () => ({
            buildings: parseNames(buildingNames, buildingCount, "Gedung"),
            guards: parseNames(guardNames, guardCount, "S"),
            shifts: parseShiftNames(shiftNames),
            guardsPerShift,
            periodDays,
            minDaysOff,
        }),
        [
            buildingCount,
            buildingNames,
            guardCount,
            guardNames,
            shiftNames,
            guardsPerShift,
            periodDays,
            minDaysOff,
        ]
    );

    const handleGenerate = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await generateSchedule(payload);
            setResult(response.result);
            const cache = {
                id: response.id,
                input: payload,
                result: response.result,
                createdAt: new Date().toISOString(),
            };
            if (typeof window !== "undefined") {
                window.sessionStorage.setItem("latestSchedule", JSON.stringify(cache));
            }
        } catch (err) {
            setError(String(err));
        } finally {
            setLoading(false);
        }
    };

    return (
        <main>
            <div className="page">
                <header className="hero">
                    <h1>Satpam Scheduler</h1>
                    <p>
                        Buat jadwal shift satpam secara otomatis dengan algoritma genetika.
                        Masukkan parameter, kirim ke backend, dan lihat hasilnya.
                    </p>
                </header>

                <div className="grid">
                    <BuildingInput
                        buildingCount={buildingCount}
                        buildingNames={buildingNames}
                        onBuildingCountChange={setBuildingCount}
                        onBuildingNamesChange={setBuildingNames}
                    />
                    <GuardInput
                        guardCount={guardCount}
                        guardNames={guardNames}
                        onGuardCountChange={setGuardCount}
                        onGuardNamesChange={setGuardNames}
                    />
                    <ShiftInput
                        shiftNames={shiftNames}
                        guardsPerShift={guardsPerShift}
                        periodDays={periodDays}
                        minDaysOff={minDaysOff}
                        onShiftNamesChange={setShiftNames}
                        onGuardsPerShiftChange={setGuardsPerShift}
                        onPeriodDaysChange={setPeriodDays}
                        onMinDaysOffChange={setMinDaysOff}
                    />
                    <section className="card">
                        <h3>Aksi</h3>
                        <div className="field">
                            <label className="label">Kirim ke backend</label>
                            <button className="button" onClick={handleGenerate} disabled={loading}>
                                {loading ? "Memproses..." : "Generate Jadwal"}
                            </button>
                        </div>
                        {result && (
                            <button
                                className="button secondary"
                                onClick={() => router.push("/result")}
                                disabled={loading}
                            >
                                Buka Halaman Result
                            </button>
                        )}
                        {error && <p className="notice">{error}</p>}
                    </section>
                </div>

                {result?.warnings?.length ? (
                    <section className="notice">
                        <strong>Warning:</strong> {result.warnings.join(" ")}
                    </section>
                ) : null}

                {result ? (
                    <section className="card">
                        <h3>Ringkasan Fitness</h3>
                        <div className="metrics">
                            <div>Fitness score: {result.fitnessScore.toFixed(2)}</div>
                            <div>Kurang satpam/shift: {result.metrics.missingGuards}</div>
                            <div>Double shift/hari: {result.metrics.doubleShiftDays}</div>
                            <div>
                                Overlap shift/gedung: {result.metrics.overlapShiftAssignments ?? 0}
                            </div>
                            <div>Kekurangan libur: {result.metrics.dayOffShortage}</div>
                            <div>Stdev beban: {result.metrics.workloadStdev.toFixed(2)}</div>
                        </div>
                    </section>
                ) : null}

                <div className="tables">
                    <ScheduleTable rows={result?.schedule ?? []} />
                    <GuardSummaryTable summaries={result?.guardSummary ?? []} />
                </div>
            </div>
        </main>
    );
}
