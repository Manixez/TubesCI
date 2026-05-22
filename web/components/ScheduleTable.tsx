import { ScheduleRow } from "../types/schedule";

type ScheduleTableProps = {
    rows: ScheduleRow[];
};

export default function ScheduleTable({ rows }: ScheduleTableProps) {
    if (rows.length === 0) {
        return (
            <section className="card">
                <h3>Jadwal</h3>
                <p>Belum ada jadwal untuk ditampilkan.</p>
            </section>
        );
    }

    const grouped = new Map<string, ScheduleRow[]>();
    for (const row of rows) {
        if (!grouped.has(row.building)) {
            grouped.set(row.building, []);
        }
        grouped.get(row.building)!.push(row);
    }

    return (
        <>
            {Array.from(grouped.entries()).map(([building, buildingRows]) => (
                <section className="card" key={building}>
                    <h3>{building}</h3>
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Hari</th>
                                <th>Shift</th>
                                <th>Satpam</th>
                            </tr>
                        </thead>
                        <tbody>
                            {buildingRows.map((row, index) => (
                                <tr key={`${row.day}-${row.shift}-${index}`}>
                                    <td>{row.day}</td>
                                    <td>{row.shift}</td>
                                    <td>
                                        <div className="tags">
                                            {row.guards.map((guard) => (
                                                <span
                                                    key={`${row.day}-${row.shift}-${guard}`}
                                                    className="tag"
                                                >
                                                    {guard}
                                                </span>
                                            ))}
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </section>
            ))}
        </>
    );
}
