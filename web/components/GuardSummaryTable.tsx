import { GuardSummary } from "../types/schedule";

type GuardSummaryTableProps = {
    summaries: GuardSummary[];
};

const buildDailyText = (summary: GuardSummary): string => {
    const lines = (summary.dailyAssignments ?? []).map((daily) => {
        const shiftsText = daily.shifts
            .map((shift) => `${shift.shift} (${shift.building})`)
            .join(", ");
        return `${daily.day}: ${shiftsText}`;
    });

    return `Satpam: ${summary.name}\n${lines.join("\n")}`.trim();
};

const copyText = async (text: string): Promise<void> => {
    if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(text);
        return;
    }

    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
};

export default function GuardSummaryTable({ summaries }: GuardSummaryTableProps) {
    if (summaries.length === 0) {
        return (
            <section className="card">
                <h3>Ringkasan Satpam</h3>
                <p>Belum ada ringkasan untuk ditampilkan.</p>
            </section>
        );
    }

    return (
        <section className="card">
            <h3>Ringkasan Satpam</h3>
            <table className="table">
                <thead>
                    <tr>
                        <th>Satpam</th>
                        <th>Total Shift</th>
                        <th>Gedung</th>
                        <th>Rincian Harian</th>
                        <th>Keterangan</th>
                    </tr>
                </thead>
                <tbody>
                    {summaries.map((summary) => (
                        <tr key={summary.name}>
                            <td>
                                <div className="summary-name">
                                    <span>{summary.name}</span>
                                    <button
                                        className="copy-button"
                                        type="button"
                                        onClick={() => copyText(buildDailyText(summary))}
                                    >
                                        Copy
                                    </button>
                                </div>
                            </td>
                            <td>{summary.totalShifts}</td>
                            <td>{summary.buildings.join(", ") || "-"}</td>
                            <td>
                                <div className="daily-list">
                                    {(summary.dailyAssignments ?? []).map((daily) => {
                                        const shiftsText = daily.shifts
                                            .map((shift) => `${shift.shift} (${shift.building})`)
                                            .join(", ");
                                        return (
                                            <div key={daily.day} className="daily-item">
                                                <strong>{daily.day}:</strong> {shiftsText}
                                            </div>
                                        );
                                    })}
                                </div>
                            </td>
                            <td>{summary.label}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </section>
    );
}
