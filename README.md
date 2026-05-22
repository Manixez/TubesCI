# Satpam Scheduler

Modular monorepo untuk penjadwalan shift satpam dengan tiga bagian utama:
- `web/` (Next.js) sebagai frontend
- `backend/` (Vercel Functions + TypeScript) sebagai API
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
    "overlapShiftAssignments": 0,
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
Buat env untuk koneksi database PostgreSQL + GA API:
```
DATABASE_URL=postgresql://user:password@localhost:5432/satpam
GA_API_URL=http://localhost:8000
CORS_ORIGIN=http://localhost:3000
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

## Deployment
### A) Deploy GA (FastAPI) ke Render/Railway/Fly
1) Pilih repo ini, set **Root Directory** ke `ga_engine`.
2) Build command:
```bash
pip install -r requirements.txt
```
3) Start command:
```bash
uvicorn ga_engine.api.app:app --host 0.0.0.0 --port 8000
```
4) Catat URL public-nya, nanti dipakai sebagai `GA_API_URL` di backend.

### B) Deploy Backend (Vercel Functions)
1) Buat project baru di Vercel, set **Root Directory** ke `backend`.
2) Tambahkan env vars:
```
DATABASE_URL=postgresql://user:password@host:5432/db
GA_API_URL=https://your-ga-service.onrender.com
CORS_ORIGIN=https://your-frontend.vercel.app
```
3) Deploy. Endpoint tersedia di `/api/schedule/*`.

### C) Deploy Frontend (Vercel)
1) Buat project baru di Vercel, set **Root Directory** ke `web`.
2) Tambahkan env var:
```
NEXT_PUBLIC_API_BASE_URL=https://your-backend.vercel.app
```
3) Deploy.
