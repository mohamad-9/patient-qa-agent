import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# -------------------------------------------------------------------
# Hugging Face Router (OpenAI-compatible) Configuration
# -------------------------------------------------------------------

HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("HUGGINGFACE_API_TOKEN is not set")

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=HF_TOKEN,
)

# Model id (from your HF router)
MODEL_ID = "ServiceNow-AI/Apriel-1.6-15b-Thinker"

DISCLAIMER = "This is for educational purposes only and not medical advice."

# Generic, safe fallback answer (no directives, no specifics)
FALLBACK = (
    "Some medical conditions can influence how the body regulates fluids, energy use, "
    "and circulation, which may contribute to symptoms such as fatigue, increased thirst, "
    "or headaches in a general way. These effects can relate to how the body manages glucose, "
    "hormones, and hydration levels. Healthcare professionals consider the full clinical "
    "picture when interpreting symptoms like these. "
    + DISCLAIMER
)

# Markers that indicate chain-of-thought / reasoning leakage
REASONING_MARKERS = [
    "Here are my reasoning steps",
    "My reasoning",
    "Let's think step by step",
    "Chain-of-thought",
    "Chain of thought",
    "Reasoning:",
    "we need to",
    "so we need to",
    "therefore we need",
    "i will",
    "we must",
]

# Markers that indicate advice / directives we want to remove
ADVICE_MARKERS = [
    "you should",
    "try to",
    "i recommend",
    "recommend",
    "managing",
    "manage ",
    "stay hydrated",
    "drink water",
    "get adequate",
    "exercise",
    "take ",
    "avoid ",
    "start ",
    "stop ",
    "cut down",
    "reduce ",
    "increase ",
    "talk to your doctor",
]


def _has_reasoning(text: str) -> bool:
    t = (text or "").strip().lower()
    if t.startswith("we need") or t.startswith("so we need"):
        return True
    return any(marker.lower() in t for marker in REASONING_MARKERS)


def _looks_like_advice(text: str) -> bool:
    t = (text or "").lower()
    return any(marker in t for marker in ADVICE_MARKERS)


def _is_disclaimer_only(text: str) -> bool:
    if not text:
        return True
    t = re.sub(r"\s+", " ", text).strip()
    d = DISCLAIMER.strip()
    return (t == d) or (t == f"{d}.") or (len(t) <= len(d) + 2)


def _clean_to_final_answer(text: str) -> str:
    """
    Best-effort cleanup:
    - Remove obvious reasoning blocks / meta instructions
    - Ensure final disclaimer sentence exists exactly once at the end
    """
    if not text:
        return FALLBACK

    # Remove obvious planning / reasoning paragraphs (heuristics)
    text = re.sub(r"(?is)here are my reasoning steps:.*?(?=\n\n|$)", "", text).strip()
    text = re.sub(r"(?im)^(we need|so we need|therefore we need).*$", "", text).strip()

    # Remove meta lines
    text = re.sub(r"(?im)^we must.*$", "", text).strip()
    text = re.sub(r"(?im)^thus we need.*$", "", text).strip()

    # Remove any existing disclaimer duplicates
    text = re.sub(re.escape(DISCLAIMER), "", text).strip()

    # If we accidentally wiped everything, return fallback
    if not text:
        return FALLBACK

    # Ensure we end with the exact disclaimer as the last sentence
    if not text.endswith(DISCLAIMER):
        if text and not text.endswith((".", "!", "?")):
            text += "."
        text = text.strip() + " " + DISCLAIMER

    return text.strip()


def _call_chat(messages, max_tokens=220, temperature=0.0) -> str:
    """
    Thin wrapper around OpenAI-compatible chat completion API.
    """
    resp = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return (resp.choices[0].message.content or "").strip()


# -------------------------------------------------------------------
# Public API: query_huggingface(prompt)
# -------------------------------------------------------------------
def query_huggingface(prompt: str) -> str:
    """
    3-pass defense:
    - Pass 1: generate educational-only answer (no reasoning)
    - Pass 2: if reasoning leaks, rewrite as final answer only
    - Pass 3: if advice/directives appear, rewrite to remove ALL advice
    - Final: sanitize and fallback if any instructions leak
    """
    try:
        # -----------------------
        # PASS 1 (Primary)
        # -----------------------
        system_1 = (
            "You are an educational assistant.\n"
            "SAFETY RULES:\n"
            "- Do NOT diagnose diseases.\n"
            "- Do NOT recommend treatments or medications.\n"
            "- Do NOT give personalized medical advice.\n"
            "- Do NOT give action advice or directives (no 'do X', 'try Y', 'you should').\n"
            "- Provide general medical education only.\n\n"
            "OUTPUT RULES:\n"
            "- Do NOT reveal reasoning steps or analysis.\n"
            "- Write 4–6 sentences of educational explanation.\n"
            f"- Then add this exact final sentence as the last sentence: {DISCLAIMER}\n"
            "- Output only the final answer text.\n"
        )

        answer_1 = _call_chat(
            messages=[
                {"role": "system", "content": system_1},
                {"role": "user", "content": prompt},
            ],
            max_tokens=220,
            temperature=0.0,
        )

        if (
            (not _has_reasoning(answer_1))
            and (not _looks_like_advice(answer_1))
            and (not _is_disclaimer_only(answer_1))
        ):
            return _clean_to_final_answer(answer_1)

        # -----------------------
        # PASS 2 (Rewrite: remove reasoning)
        # -----------------------
        system_2 = (
            "Rewrite into a clean final answer.\n"
            "RULES:\n"
            "- Do NOT include reasoning, analysis, steps, or meta commentary.\n"
            "- Do NOT include phrases like 'We need to' or planning.\n"
            "- Do NOT give action advice or directives.\n"
            "- Write 4–6 sentences.\n"
            f"- Then add this exact final sentence as the last sentence: {DISCLAIMER}\n"
            "- Output only the final answer text.\n"
        )

        answer_2 = _call_chat(
            messages=[
                {"role": "system", "content": system_2},
                {
                    "role": "user",
                    "content": (
                        "Original prompt:\n"
                        f"{prompt}\n\n"
                        "Bad response:\n"
                        f"{answer_1}\n\n"
                        "Now rewrite as final answer only."
                    ),
                },
            ],
            max_tokens=220,
            temperature=0.0,
        )

        if (
            (not _has_reasoning(answer_2))
            and (not _looks_like_advice(answer_2))
            and (not _is_disclaimer_only(answer_2))
        ):
            return _clean_to_final_answer(answer_2)

        # -----------------------
        # PASS 3 (Rewrite: remove ALL advice)
        # -----------------------
        system_3 = (
            "Rewrite to remove ALL advice.\n"
            "RULES:\n"
            "- Explain only general mechanisms and what doctors commonly discuss.\n"
            "- Do NOT tell the user to do anything.\n"
            "- Do NOT recommend treatments or medications.\n"
            "- Write 4–6 sentences.\n"
            f"- Then add this exact final sentence as the last sentence: {DISCLAIMER}\n"
            "- Output only the final answer text.\n"
        )

        answer_3 = _call_chat(
            messages=[
                {"role": "system", "content": system_3},
                {
                    "role": "user",
                    "content": (
                        "Original prompt:\n"
                        f"{prompt}\n\n"
                        "Response that contains advice/reasoning:\n"
                        f"{answer_2}\n\n"
                        "Now rewrite with NO advice and no reasoning."
                    ),
                },
            ],
            max_tokens=220,
            temperature=0.0,
        )

        final_text = _clean_to_final_answer(answer_3)

        # -------------------------------------------------
        # Final safety cleanup: NEVER leak instructions
        # -------------------------------------------------
        forbidden_fragments = [
            "Rewrite to remove ALL advice",
            "Rewrite into a clean final answer",
            "OUTPUT RULES",
            "Chain-of-thought",
            "Chain of thought",
            "Reasoning:",
            "Now rewrite",
            "as the last sentence",
        ]

        lowered = final_text.lower()
        if any(fragment.lower() in lowered for fragment in forbidden_fragments):
            return FALLBACK

        # If it is still broken, use safe fallback
        if _is_disclaimer_only(final_text) or _has_reasoning(final_text):
            return FALLBACK

        return final_text

    except Exception as e:
        # For debugging you might prefer to return the error;
        # if you want to hide errors from end users, change this to `return FALLBACK`.
        return f"Hugging Face API client error: {repr(e)}"


# -------------------------------------------------------------------
# Optional compatibility wrapper: query_huggingface_chat
# -------------------------------------------------------------------
def query_huggingface_chat(user_messages: list[dict]) -> str:
    """
    Compatibility helper if you ever want to call the model using a list
    of chat-style messages instead of a single prompt string.

    user_messages example:
    [
      {"role": "user", "content": "Why do I feel tired?"},
      {"role": "assistant", "content": "..." },
      ...
    ]

    We convert them into a text prompt and delegate to query_huggingface().
    """
    lines = []
    for m in user_messages or []:
        role = m.get("role", "user")
        content = (m.get("content") or "").strip()
        if not content:
            continue
        label = "Patient" if role == "user" else "Assistant"
        lines.append(f"{label}: {content}")

    if not lines:
        # If nothing useful, just pass an empty prompt
        return query_huggingface("")

    prompt = "\n".join(lines)
    return query_huggingface(prompt)
