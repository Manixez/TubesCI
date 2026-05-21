import { GuardSummary } from "../types/schedule";

type GuardSummaryTableProps = {
    summaries: GuardSummary[];
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
                        <th>Keterangan</th>
                    </tr>
                </thead>
                <tbody>
                    {summaries.map((summary) => (
                        <tr key={summary.name}>
                            <td>{summary.name}</td>
                            <td>{summary.totalShifts}</td>
                            <td>{summary.buildings.join(", ") || "-"}</td>
                            <td>{summary.label}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </section>
    );
}
