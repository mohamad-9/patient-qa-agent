from pydantic import BaseModel
from typing import List

class QuestionRequest(BaseModel):
    medical_history: str
    diagnoses: List[str]
    symptoms: List[str]
    question: str

class AnswerResponse(BaseModel):
    answer: str
    note: str  # always includes educational disclaimer
