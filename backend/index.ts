import express from "express";
import cors from "cors";

import { generateSchedule } from "./api/generate-schedule";
import { getLatestScheduleHandler, getScheduleHandler } from "./api/get-schedule";
import { saveScheduleHandler } from "./api/save-schedule";
import { initDb } from "./services/scheduleService";

const app = express();
const port = Number(process.env.PORT || 4000);

app.use(
    cors({
        origin: process.env.CORS_ORIGIN?.split(",").map((item) => item.trim()) || "*",
    })
);
app.use(express.json({ limit: "2mb" }));

app.get("/health", (_req, res) => {
    res.json({ status: "ok" });
});

app.post("/api/schedule/generate", generateSchedule);
app.post("/api/schedule/save", saveScheduleHandler);
app.get("/api/schedule/latest", getLatestScheduleHandler);
app.get("/api/schedule/:id", getScheduleHandler);

initDb()
    .then(() => {
        app.listen(port, () => {
            console.log(`Backend listening on port ${port}`);
        });
    })
    .catch((err) => {
        console.error("Gagal inisialisasi database:", err);
        process.exit(1);
    });
