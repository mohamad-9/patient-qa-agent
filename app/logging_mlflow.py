import os
import time
import mlflow

# Where to store runs locally (safe + simple)
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "patient-qa-agent")
mlflow.set_experiment(EXPERIMENT_NAME)


def log_ask_run(
    *,
    model_id: str,
    is_blocked: bool,
    latency_ms: int,
    symptoms_count: int,
    conditions_count: int,
    diagnoses_count: int,
    error: str | None = None,
):
    """
    Logs ONLY safe metadata. Do NOT log raw medical history, symptoms text, or user questions.
    """
    with mlflow.start_run():
        mlflow.log_param("model_id", model_id)
        mlflow.log_param("is_blocked", is_blocked)

        mlflow.log_metric("latency_ms", latency_ms)
        mlflow.log_metric("symptoms_count", symptoms_count)
        mlflow.log_metric("conditions_count", conditions_count)
        mlflow.log_metric("diagnoses_count", diagnoses_count)

        if error:
            mlflow.log_param("error", error[:200])  # keep short
