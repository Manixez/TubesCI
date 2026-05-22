FROM python:3.12-slim

WORKDIR /app

COPY . /app/ga_engine

RUN pip install --no-cache-dir -r /app/ga_engine/requirements.txt

ENV PYTHONPATH=/app
ENV PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "uvicorn ga_engine.api.app:app --host 0.0.0.0 --port ${PORT:-8000}"]
