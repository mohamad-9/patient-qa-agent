# app/main.py
from dotenv import load_dotenv

load_dotenv()

import os
import time

from fastapi import FastAPI, Response

from app.ui import router as ui_router
from app.schemas import QuestionRequest, AnswerResponse
from app.nlp import extract_conditions, extract_symptoms
from app.safety import check_safety
from app.logging_mlflow import log_ask_run
from app.models import query_huggingface_chat, MODEL_ID

# ---------------------------------------------------------
# FastAPI app (this is what uvicorn looks for)
# ---------------------------------------------------------
app = FastAPI(
    title="Patient Medical History Q&A Assistant (Non-Clinical)",
    description=(
        "Healthcare-safe AI assistant that answers educational questions "
        "based on user-provided medical history and diagnoses."
    ),
    version="0.2.0",
)

# UI demo page (/demo)
app.include_router(ui_router)


# ---------------------------------------------------------
# Simple endpoints
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# Main /ask endpoint (chat-style, with context)
# ---------------------------------------------------------
@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest, response: Response):
    """
    Main educational Q&A endpoint.
    - Enforces question presence
    - Enforces context unless allow_no_context=True
    - Runs safety gate
    - Builds chat-style context for the model
    - Logs only safe metadata to MLflow
    """
    start = time.perf_counter()
    error_msg = None

    try:
        # 1) HARD GUARD: require a question
        if not request.question or not request.question.strip():
            response.status_code = 400
            return AnswerResponse(
                answer=(
                    "Please provide a question. The system only responds when a question is provided. "
                    "This is for educational purposes only and not medical advice."
                ),
                note="This explanation is for educational purposes only and not medical advice.",
            )

        # 2) HARD GUARD: require medical context
        #    (at least one of history / diagnoses / symptoms),
        #    unless allow_no_context=True is set (for generic tests)
        has_context = any(
            [
                bool((request.medical_history or "").strip()),
                bool(request.diagnoses),
                bool(request.symptoms),
            ]
        )

        if not has_context and not getattr(request, "allow_no_context", False):
            response.status_code = 400
            return AnswerResponse(
                answer=(
                    "Please provide at least one of the following before asking a question:\n"
                    "• medical history\n"
                    "• diagnoses\n"
                    "• symptoms\n\n"
                    "This assistant can only explain questions in the context of "
                    "user-provided medical information. "
                    "This is for educational purposes only and not medical advice."
                ),
                note="This explanation is for educational purposes only and not medical advice.",
            )

        # 3) Safety gate (blocks diagnosis / treatment advice / medication changes)
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
                note="This explanation is for educational purposes only and not medical advice.",
            )

        # 4) NLP extraction (simple keyword-based from medical_history)
        conditions = extract_conditions(request.medical_history or "")
        symptoms_found = extract_symptoms(request.medical_history or "")

        # 5) Build chat-style context (for this request only, not persisted)
        context_block = (
            "User-provided context (do not diagnose; explain educationally only):\n"
            f"- Medical history: {request.medical_history or '(none)'}\n"
            f"- Known diagnoses: {request.diagnoses or []}\n"
            f"- Symptoms list (form): {request.symptoms or []}\n"
            f"- Extracted conditions (NLP): {conditions or []}\n"
            f"- Extracted symptoms (NLP): {symptoms_found or []}\n"
        )

        # Frontend chat messages (already trimmed to short history, but we enforce again)
        incoming = getattr(request, "messages", []) or []
        incoming = incoming[-8:]  # keep last 8 messages max

        # This list is passed to query_huggingface_chat, which will add its own system prompt
        chat_messages = [
            {"role": "user", "content": context_block},
        ]

        # Add prior conversation turns
        for m in incoming:
            # m is a Pydantic model; use its fields
            chat_messages.append({"role": m.role, "content": m.content})

        # Final user question (always last)
        chat_messages.append({"role": "user", "content": request.question.strip()})

        # 6) LLM call (chat-based with multi-turn context)
        answer_text = query_huggingface_chat(chat_messages)

        latency_ms = int((time.perf_counter() - start) * 1000)
        response.headers["x-latency-ms"] = str(latency_ms)

        # 7) Log safe metadata only (no raw text)
        log_ask_run(
            model_id=MODEL_ID,
            is_blocked=False,
            latency_ms=latency_ms,
            symptoms_count=len(symptoms_found) if symptoms_found else 0,
            conditions_count=len(conditions) if conditions else 0,
            diagnoses_count=len(request.diagnoses or []),
            error=None,
        )

        return AnswerResponse(
            answer=answer_text,
            note="This explanation is for educational purposes only and not medical advice.",
        )

    except Exception as e:
        # 8) Error handling + logging (no PHI)
        error_msg = repr(e)
        latency_ms = int((time.perf_counter() - start) * 1000)
        response.headers["x-latency-ms"] = str(latency_ms)

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
            note="This explanation is for educational purposes only and not medical advice.",
        )
