from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Response
from app.ui import router as ui_router

from app.schemas import QuestionRequest, AnswerResponse
from app.nlp import extract_conditions, extract_symptoms
from app.safety import check_safety
from app.logging_mlflow import log_ask_run
from app.models import query_huggingface, MODEL_ID

import time
import os


app = FastAPI(
    title="Patient Medical History Q&A Assistant (Non-Clinical)",
    description="Healthcare-safe AI assistant that answers educational questions based on user-provided medical history and diagnoses.",
    version="0.1.0"
)

# UI demo page (/demo)
app.include_router(ui_router)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Server is running!"}


@app.get("/debug/token")
def debug_token():
    t = os.getenv("HUGGINGFACE_API_TOKEN")
    return {"token_loaded": bool(t), "token_prefix": (t[:6] if t else None)}


@app.get("/")
def root():
    return {"status": "ok", "service": "patient-qa-agent"}


@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest, response: Response):
    start = time.perf_counter()
    error_msg = None

    try:
        # -------------------------------------------------
        # 1) HARD GUARD: require a question
        # -------------------------------------------------
        if not request.question or not request.question.strip():
            response.status_code = 400
            return AnswerResponse(
                answer=(
                    "Please provide a question. The system only responds when a question is provided. "
                    "This is for educational purposes only and not medical advice."
                ),
                note="This explanation is for educational purposes only and not medical advice."
            )

        # -------------------------------------------------
        # 2) HARD GUARD: require medical context
        #    (at least one of history / diagnoses / symptoms)
        # -------------------------------------------------
        has_context = any([
            bool((request.medical_history or "").strip()),
            bool(request.diagnoses),
            bool(request.symptoms),
        ])

        if not has_context:
            response.status_code = 400
            return AnswerResponse(
                answer=(
                    "Please provide at least one of the following before asking a question:\n"
                    "• medical history\n"
                    "• diagnoses\n"
                    "• symptoms\n\n"
                    "This assistant can only explain questions in the context of user-provided medical information. "
                    "This is for educational purposes only and not medical advice."
                ),
                note="This explanation is for educational purposes only and not medical advice."
            )

        # -------------------------------------------------
        # 3) Safety gate (blocks diagnosis / treatment advice)
        # -------------------------------------------------
        refusal = check_safety(request.question)
        if refusal:
            latency_ms = int((time.perf_counter() - start) * 1000)
            response.headers["x-latency-ms"] = str(latency_ms)

            # Log safe metadata only (no PHI)
            log_ask_run(
                model_id=MODEL_ID,
                is_blocked=True,
                latency_ms=latency_ms,
                symptoms_count=0,
                conditions_count=0,
                diagnoses_count=len(request.diagnoses or []),
                error=None,
            )

            return AnswerResponse(
                answer=refusal,
                note="This explanation is for educational purposes only and not medical advice."
            )

        # -------------------------------------------------
        # 4) NLP extraction (simple keyword-based)
        # -------------------------------------------------
        conditions = extract_conditions(request.medical_history or "")
        symptoms = extract_symptoms(request.medical_history or "")

        # -------------------------------------------------
        # 5) Prompt
        # -------------------------------------------------
        prompt = (
            f"Known diagnoses (user-provided): {request.diagnoses}\n"
            f"Symptoms mentioned: {symptoms}\n"
            f"Question: {request.question}\n"
            "Explain simply in 4–6 sentences."
        )

        # -------------------------------------------------
        # 6) LLM call
        # -------------------------------------------------
        answer_text = query_huggingface(prompt)

        latency_ms = int((time.perf_counter() - start) * 1000)
        response.headers["x-latency-ms"] = str(latency_ms)

        # -------------------------------------------------
        # 7) Log safe metadata only (no PHI)
        # -------------------------------------------------
        log_ask_run(
            model_id=MODEL_ID,
            is_blocked=False,
            latency_ms=latency_ms,
            symptoms_count=len(symptoms) if symptoms else 0,
            conditions_count=len(conditions) if conditions else 0,
            diagnoses_count=len(request.diagnoses or []),
            error=None,
        )

        return AnswerResponse(
            answer=answer_text,
            note="This explanation is for educational purposes only and not medical advice."
        )

    except Exception as e:
        error_msg = repr(e)
        latency_ms = int((time.perf_counter() - start) * 1000)
        response.headers["x-latency-ms"] = str(latency_ms)

        # Log failure (still no PHI)
        log_ask_run(
            model_id=MODEL_ID,
            is_blocked=False,
            latency_ms=latency_ms,
            symptoms_count=0,
            conditions_count=0,
            diagnoses_count=len(request.diagnoses or []),
            error=error_msg,
        )

        response.status_code = 500
        return AnswerResponse(
            answer=f"Internal error: {error_msg}",
            note="This explanation is for educational purposes only and not medical advice."
        )
