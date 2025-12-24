# 🩺 Patient Medical History Q&A Assistant (Non-Clinical)

A **health-safe, educational AI assistant** that explains medical topics **without providing diagnosis, treatment, or personal medical advice**.

This project demonstrates how to design **responsible AI systems** that handle **sensitive healthcare topics safely** — with **multi-turn chat**, **strict refusal rules**, and **privacy-aware logging**.

> ⚠️ This system is **NOT a medical device** and **NOT a substitute for professional medical advice**.

---

## 🆕 Current Version

### ✅ v0.2 — Chat Assistant Release

✔ Chat-style conversation UI  
✔ Conversation context preserved  
✔ Strong safety guardrails  
✔ Hugging Face Router API  
✔ MLflow metadata logging (no PHI stored)  
✔ Docker-ready & deployable  
✔ Dev-mode toggle for testing

---

## 🎯 Project Goals

Built to learn:

- Safe AI Assistant design
- Preventing unsafe medical outputs
- FastAPI backend architecture
- NLP context extraction
- Docker deployment
- Cloud hosting practices
- Privacy-first logging approach

---

## 💬 What the Assistant CAN Do

✔ Explain doctor-provided diagnoses  
✔ Explain medical terms  
✔ Describe general health mechanisms  
✔ Provide educational answers  
✔ Maintain conversation context  
✔ Refuse unsafe requests politely  

---

## 🚫 What the Assistant Will NOT Do

❌ Diagnose  
❌ Recommend medications  
❌ Suggest treatments  
❌ Give personal health advice  
❌ Replace a doctor  

Unsafe questions trigger a refusal response.

---

## 🧠 Safety Architecture

### 🔹 Frontend
Input validation + chat guardrails

### 🔹 Backend
Validation + structured schema checks

### 🔹 Safety Classifier
Blocks:
- Treatment advice
- Diagnosis questions
- Medication guidance
- Urgent care advice

### 🔹 Prompt Rules
- Educational only
- No reasoning exposed
- Disclaimer always added

### 🔹 Privacy Logging
MLflow stores ONLY:
- latency
- counts
- flags
- model id

❌ No medical text stored  
❌ No PHI stored

---

## 🌐 Live Example (if deployed)

Demo UI:
```
https://your-service-url/demo
```

API Docs (Swagger):
```
https://your-service-url/docs
```

---

## 🛠 Tech Stack

| Layer | Tool |
|------|-----|
| Backend | FastAPI |
| Server | Uvicorn |
| Model | Hugging Face Router |
| NLP | spaCy |
| Logging | MLflow |
| Runtime | Python 3.11 |
| Container | Docker |
| Hosting | Render |

---

## 🔐 Environment Variables

Create `.env`

```
HUGGINGFACE_API_TOKEN=hf_xxxxxxxxx
MLFLOW_TRACKING_URI=file:/app/mlruns
MLFLOW_EXPERIMENT_NAME=patient-qa-agent
```

---

## ▶️ Run Local

```
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```
http://127.0.0.1:8000/demo
```

---

## 🐳 Docker

```
docker build -t patient-qa-agent .
docker run -p 8000:8000 --env-file .env patient-qa-agent
```

---

## 📡 API Example

POST `/ask`

```json
{
  "medical_history": "Diagnosed with type 2 diabetes last year.",
  "diagnoses": ["Type 2 Diabetes"],
  "symptoms": ["fatigue", "increased thirst"],
  "question": "Why do I feel tired?",
  "messages": []
}
```

Response includes disclaimer.

---

## 📘 Disclaimer

> This is for educational purposes only and not medical advice.

---

## 🔮 Future Work

- Conversation history persistence
- Sidebar chat list
- Better UI polish
- Extended NLP

---

## 📜 License
Educational & learning use only.
