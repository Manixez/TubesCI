# Satpam Scheduler

Modular monorepo untuk penjadwalan shift satpam dengan tiga bagian utama:
- `web/` (Next.js) sebagai frontend
- `backend/` (Express + TypeScript) sebagai API
- `ga_engine/` (Python) sebagai mesin GA

## Struktur
```
web/
  app/
  components/
  services/
  types/
backend/
  api/
  services/
  validators/
  types/
ga_engine/
  main.py
  models/
  ga/
  services/
  api/
```

## API Contract
**Input**
```json
{
  "buildings": ["Gedung A", "Gedung B"],
  "guards": ["S01", "S02"],
  "shifts": ["Shift 1", "Shift 2"],
  "guardsPerShift": 2,
  "periodDays": 7,
  "minDaysOff": 2
}
```

**Output**
```json
{
  "schedule": [{"day":"Senin","building":"Gedung A","shift":"Shift 1","guards":["S01","S02"]}],
  "guardSummary": [{"name":"S01","totalShifts":5,"buildings":["Gedung A"],"label":"Beban normal"}],
  "warnings": ["Jumlah satpam tidak mencukupi ..."],
  "fitnessScore": 120.5,
  "metrics": {
    "missingGuards": 0,
    "doubleShiftDays": 0,
    "dayOffShortage": 0,
    "workloadStdev": 1.1,
    "buildingRepeatExcess": 0.0,
    "totalPenalty": 120.5
  }
}
```

## Menjalankan (Dev)
### 1) Python GA
```bash
cd ga_engine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Backend
```bash
cd backend
npm install
```
Buat env untuk koneksi database PostgreSQL:
```
DATABASE_URL=postgresql://user:password@localhost:5432/satpam
GA_PYTHON=python3
```
Jalankan:
```bash
npm run dev
```

### 3) Frontend
```bash
cd web
npm install
```
Tambahkan env (opsional):
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:4000
```
Jalankan:
```bash
npm run dev
```

## Catatan
- Backend akan menyimpan hasil jadwal ke PostgreSQL pada tabel `schedules`.
- Frontend menampilkan form input, tabel jadwal, ringkasan satpam, dan warning.
- File Python lama (di root) masih ada; jika sudah yakin, bisa dipindahkan atau dihapus manual.
