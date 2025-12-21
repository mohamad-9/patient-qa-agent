import spacy
from typing import List

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define a simple list of medical keywords for demo
CONDITIONS = ["diabetes", "hypertension", "asthma", "cancer"]
SYMPTOMS = ["fatigue", "thirst", "cough", "headache"]

def extract_conditions(text: str) -> List[str]:
    """
    Extract known medical conditions from text using keyword matching.
    """
    doc = nlp(text.lower())
    found = [cond for cond in CONDITIONS if cond in doc.text]
    return found

def extract_symptoms(text: str) -> List[str]:
    """
    Extract known symptoms from text using keyword matching.
    """
    doc = nlp(text.lower())
    found = [symptom for symptom in SYMPTOMS if symptom in doc.text]
    return found
