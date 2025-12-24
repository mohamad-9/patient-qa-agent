from pydantic import BaseModel
from typing import List, Literal


class ChatMessage(BaseModel):
    """
    A single chat message from the user or assistant.

    This is only for *this request* and is not stored on the server.
    """
    role: Literal["user", "assistant"]
    content: str


class QuestionRequest(BaseModel):
    """
    Request body for /ask.

    - medical_history / diagnoses / symptoms: context for the assistant
    - question: the current user question
    - messages: short chat history (user + assistant turns)
    - allow_no_context: if True, allows asking questions with no medical context
    """
    medical_history: str = ""
    diagnoses: List[str] = []
    symptoms: List[str] = []

    question: str

    messages: List[ChatMessage] = []

    # default False → normally require context
    allow_no_context: bool = False


class AnswerResponse(BaseModel):
    """
    Response body from /ask.
    """
    answer: str
    note: str  # always includes educational disclaimer
