import re
from typing import Optional

DISCLAIMER = "This explanation is for educational purposes only and not medical advice."

# -----------------------------
# Unsafe intent patterns
# -----------------------------

DIAGNOSIS_PATTERNS = [
    r"\bdo i have\b",
    r"\bdo i suffer from\b",
    r"\bam i diagnosed with\b",
    r"\bwhat disease do i have\b",
    r"\bwhat condition do i have\b",
]

TREATMENT_PATTERNS = [
    r"\bwhat should i take\b",
    r"\bwhat medicine\b",
    r"\bwhat medication\b",
    r"\btreatment for\b",
    r"\bhow do i treat\b",
    r"\bhow to cure\b",
]

MEDICATION_CHANGE_PATTERNS = [
    r"\bshould i stop\b",
    r"\bshould i start\b",
    r"\bchange my medication\b",
    r"\bincrease dosage\b",
    r"\bdecrease dosage\b",
]

ACTION_ADVICE_PATTERNS = [
    r"\bwhat should i do\b",
    r"\bwhat can i do\b",
    r"\bhow should i\b",
]

ALL_UNSAFE_PATTERNS = (
    DIAGNOSIS_PATTERNS
    + TREATMENT_PATTERNS
    + MEDICATION_CHANGE_PATTERNS
    + ACTION_ADVICE_PATTERNS
)


# -----------------------------
# Safety check function
# -----------------------------

def check_safety(question: str) -> Optional[str]:
    """
    Returns a refusal message if the question is unsafe.
    Returns None if the question is allowed.
    """
    q = question.lower()

    for pattern in ALL_UNSAFE_PATTERNS:
        if re.search(pattern, q):
            return (
                "I can’t help with diagnosing conditions, recommending treatments, "
                "or giving personalized medical advice. "
                "I can explain general medical information or help you prepare questions "
                "to discuss with a healthcare professional. "
                + DISCLAIMER
            )

    return None
