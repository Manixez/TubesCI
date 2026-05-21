from fastapi import FastAPI, HTTPException

from ga_engine.main import generate_schedule_from_payload

app = FastAPI(title="GA Engine API", version="1.0.0")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/generate")
async def generate(payload: dict) -> dict:
    try:
        result = generate_schedule_from_payload(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return result.to_dict()
