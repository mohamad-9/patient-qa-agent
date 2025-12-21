FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensure MLflow file store directory exists inside the container
RUN mkdir -p /app/mlruns

# Download spaCy model at build time
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8000

# App Runner provides PORT env var (we default to 8000 for local)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
