
import spacy
from typing import List

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Canonical / normalized condition names
CONDITIONS = {
    "diabetes": ["diabetes", "diabetic"],
    "hypertension": ["hypertension", "high blood pressure"],
    "asthma": ["asthma"],
    "cancer": ["cancer"],
}

SYMPTOMS = {
    "fatigue": ["fatigue", "tired", "tiredness", "exhausted"],
    "thirst": ["thirst", "thirsty"],
    "cough": ["cough", "coughing"],
    "headache": ["headache", "headaches"],
}


def normalize_words(text: str) -> List[str]:
    """
    Convert text into a list of normalized lemmas using spaCy.
    """
    doc = nlp(text.lower())
    return [token.lemma_ for token in doc if token.is_alpha]


def extract_conditions(text: str) -> List[str]:
    lemmas = normalize_words(text)

    found = []
    for condition, variants in CONDITIONS.items():
        for word in lemmas:
            if word in variants:
                found.append(condition)
                break
    return found


def extract_symptoms(text: str) -> List[str]:
    lemmas = normalize_words(text)

    found = []
    for symptom, variants in SYMPTOMS.items():
        for word in lemmas:
            if word in variants:
                found.append(symptom)
                break
    return found
