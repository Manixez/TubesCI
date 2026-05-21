type GuardInputProps = {
    guardCount: number;
    guardNames: string;
    onGuardCountChange: (value: number) => void;
    onGuardNamesChange: (value: string) => void;
};

export default function GuardInput({
    guardCount,
    guardNames,
    onGuardCountChange,
    onGuardNamesChange,
}: GuardInputProps) {
    return (
        <section className="card">
            <h3>Satpam</h3>
            <div className="field">
                <label className="label">Jumlah satpam</label>
                <input
                    className="input"
                    type="number"
                    min={1}
                    value={guardCount}
                    onChange={(event) => onGuardCountChange(Number(event.target.value))}
                />
            </div>
            <div className="field">
                <label className="label">Nama satpam (pisah koma)</label>
                <textarea
                    className="textarea"
                    value={guardNames}
                    onChange={(event) => onGuardNamesChange(event.target.value)}
                />
            </div>
        </section>
    );
}
