# ---- Base image ----
FROM python:3.11-slim

# ---- Workdir & basic env ----
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- System deps ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---- Python deps ----
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download en_core_web_sm

# ---- App code ----
COPY . .

# ---- MLflow defaults (local filesystem inside container) ----
ENV MLFLOW_TRACKING_URI=file:/app/mlruns
ENV MLFLOW_EXPERIMENT_NAME=patient-qa-agent

# ---- Expose (local dev info only) ----
EXPOSE 8000

# ---- Start command ----
# Use PORT from env if present (Render), otherwise 8000 (local)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
