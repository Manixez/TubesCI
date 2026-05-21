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

    return (
        <section className="card">
            <h3>Jadwal Rekomendasi</h3>
            <table className="table">
                <thead>
                    <tr>
                        <th>Hari</th>
                        <th>Gedung</th>
                        <th>Shift</th>
                        <th>Satpam</th>
                    </tr>
                </thead>
                <tbody>
                    {rows.map((row, index) => (
                        <tr key={`${row.day}-${row.building}-${row.shift}-${index}`}>
                            <td>{row.day}</td>
                            <td>{row.building}</td>
                            <td>{row.shift}</td>
                            <td>
                                <div className="tags">
                                    {row.guards.map((guard) => (
                                        <span key={`${row.day}-${row.shift}-${guard}`} className="tag">
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
    );
}
