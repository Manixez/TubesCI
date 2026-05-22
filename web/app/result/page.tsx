"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import GuardSummaryTable from "../../components/GuardSummaryTable";
import ScheduleTable from "../../components/ScheduleTable";
import { getLatestSchedule } from "../../services/scheduleApi";
import { StoredSchedule } from "../../types/schedule";

export default function ResultPage() {
    const [data, setData] = useState<StoredSchedule | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const load = async () => {
            try {
                const cached = window.sessionStorage.getItem("latestSchedule");
                if (cached) {
                    setData(JSON.parse(cached));
                    setLoading(false);
                    return;
                }

                const latest = await getLatestSchedule();
                if (latest) {
                    setData(latest);
                }
            } catch (err) {
                setError(String(err));
            } finally {
                setLoading(false);
            }
        };

        load();
    }, []);

    return (
        <main>
            <div className="page">
                <header className="hero">
                    <h1>Hasil Jadwal</h1>
                    <p>
                        Ringkasan jadwal terakhir yang tersimpan. Jika kosong, generate jadwal
                        baru di halaman utama.
                    </p>
                    <div>
                        <Link className="button secondary" href="/">
                            Kembali ke Input
                        </Link>
                    </div>
                </header>

                {loading && <p>Memuat data...</p>}
                {error && <p className="notice">{error}</p>}

                {!loading && !data && <p>Belum ada jadwal tersimpan.</p>}

                {data?.result?.warnings?.length ? (
                    <section className="notice">
                        <strong>Warning:</strong> {data.result.warnings.join(" ")}
                    </section>
                ) : null}

                {data?.result ? (
                    <section className="card">
                        <h3>Ringkasan Fitness</h3>
                        <div className="metrics">
                            <div>Fitness score: {data.result.fitnessScore.toFixed(2)}</div>
                            <div>Kurang satpam/shift: {data.result.metrics.missingGuards}</div>
                            <div>Double shift/hari: {data.result.metrics.doubleShiftDays}</div>
                            <div>
                                Overlap shift/gedung: {data.result.metrics.overlapShiftAssignments ?? 0}
                            </div>
                            <div>Kekurangan libur: {data.result.metrics.dayOffShortage}</div>
                            <div>Stdev beban: {data.result.metrics.workloadStdev.toFixed(2)}</div>
                        </div>
                    </section>
                ) : null}

                <div className="tables">
                    <ScheduleTable rows={data?.result?.schedule ?? []} />
                    <GuardSummaryTable summaries={data?.result?.guardSummary ?? []} />
                </div>
            </div>
        </main>
    );
}
