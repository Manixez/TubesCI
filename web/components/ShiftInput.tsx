type ShiftInputProps = {
    shiftNames: string;
    guardsPerShift: number;
    periodDays: number;
    minDaysOff: number;
    onShiftNamesChange: (value: string) => void;
    onGuardsPerShiftChange: (value: number) => void;
    onPeriodDaysChange: (value: number) => void;
    onMinDaysOffChange: (value: number) => void;
};

export default function ShiftInput({
    shiftNames,
    guardsPerShift,
    periodDays,
    minDaysOff,
    onShiftNamesChange,
    onGuardsPerShiftChange,
    onPeriodDaysChange,
    onMinDaysOffChange,
}: ShiftInputProps) {
    return (
        <section className="card">
            <h3>Shift</h3>
            <div className="field">
                <label className="label">Nama shift (pisah koma)</label>
                <textarea
                    className="textarea"
                    value={shiftNames}
                    onChange={(event) => onShiftNamesChange(event.target.value)}
                />
            </div>
            <div className="field">
                <label className="label">Satpam per shift</label>
                <input
                    className="input"
                    type="number"
                    min={1}
                    value={guardsPerShift}
                    onChange={(event) => onGuardsPerShiftChange(Number(event.target.value))}
                />
            </div>
            <div className="field">
                <label className="label">Periode (hari)</label>
                <input
                    className="input"
                    type="number"
                    min={1}
                    value={periodDays}
                    onChange={(event) => onPeriodDaysChange(Number(event.target.value))}
                />
            </div>
            <div className="field">
                <label className="label">Hari libur minimum per satpam</label>
                <input
                    className="input"
                    type="number"
                    min={0}
                    value={minDaysOff}
                    onChange={(event) => onMinDaysOffChange(Number(event.target.value))}
                />
            </div>
        </section>
    );
}
