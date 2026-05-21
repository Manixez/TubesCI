type BuildingInputProps = {
    buildingCount: number;
    buildingNames: string;
    onBuildingCountChange: (value: number) => void;
    onBuildingNamesChange: (value: string) => void;
};

export default function BuildingInput({
    buildingCount,
    buildingNames,
    onBuildingCountChange,
    onBuildingNamesChange,
}: BuildingInputProps) {
    return (
        <section className="card">
            <h3>Gedung</h3>
            <div className="field">
                <label className="label">Jumlah gedung</label>
                <input
                    className="input"
                    type="number"
                    min={1}
                    value={buildingCount}
                    onChange={(event) => onBuildingCountChange(Number(event.target.value))}
                />
            </div>
            <div className="field">
                <label className="label">Nama gedung (pisah koma)</label>
                <textarea
                    className="textarea"
                    value={buildingNames}
                    onChange={(event) => onBuildingNamesChange(event.target.value)}
                />
            </div>
        </section>
    );
}
