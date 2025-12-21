# 🩺 Patient Medical History Q&A Assistant (Non-Clinical)


---

## 📌 Project Overview

This project is a **non-clinical, healthcare-safe AI assistant**.

It allows users to ask **educational questions** related to their **own medical history, diagnoses, and symptoms**, and receive **simple explanations** — without giving medical advice.

⚠️ This system is **NOT a medical tool** and **NOT a diagnostic system**.

---

## 🎯 Purpose of the Project

I built this project to learn:

- How to design **safe AI systems**
- How to prevent **medical advice or diagnosis**
- How to build APIs using **FastAPI**
- How to deploy AI apps using **Docker + cloud hosting**
- How to log AI usage **without storing sensitive data**

This is an **initial version**.  
In future updates, I plan to convert it into a **chat-style application**.

---

## ✅ What the Assistant Can Do

- Explain **medical terms** in simple language
- Explain **doctor-provided diagnoses**
- Explain general relationships between **conditions and symptoms**
- Answer **educational questions only**
- Show how to build AI systems with **safety guardrails**

---

## 🚫 What the Assistant Will NOT Do

The system will refuse to:

- ❌ Diagnose diseases
- ❌ Recommend medications
- ❌ Suggest treatments
- ❌ Give personal medical advice
- ❌ Replace a healthcare professional

If a question is unsafe, the system responds with a **polite refusal**.

---

## 🧠 Safety Design (Important)

Safety is enforced at **multiple levels**:

1. **Frontend guard**
   - The user must enter a valid question
2. **Backend guard**
   - The API rejects empty or invalid requests
3. **Safety classifier**
   - Blocks treatment / diagnosis questions
4. **Prompt constraints**
   - Educational explanations only
5. **Logging safety**
   - MLflow logs metadata only (no medical text)

---

## 🧪 Current Version

### Version: `v0.1 (Initial Release)`

Current features:
- REST API
- Demo web UI
- Single-question flow
- Educational explanations
- Dockerized deployment

Planned updates:
- Chat interface
- Conversation history
- UI improvements
- More robust NLP extraction

---

## 🌐 Live Deployment

The project is currently hosted online.

- **Demo UI**  
  https://patient-qa-agent.onrender.com/demo

- **API Documentation (Swagger)**  
  https://patient-qa-agent.onrender.com/docs

---

## 🛠️ Tech Stack

- **Python 3.11**
- **FastAPI** – backend framework
- **Uvicorn** – ASGI server
- **spaCy** – NLP extraction
- **Hugging Face Inference API**
- **MLflow** – experiment logging (no PHI)
- **Docker**
- **Render** – cloud hosting

---

## 📦 Python Dependencies

These are the libraries used in this project:

```txt
fastapi==0.115.5
uvicorn[standard]==0.32.0
pydantic==2.10.2
python-dotenv==1.0.1
requests==2.32.3
httpx==0.27.2

spacy==3.8.2
openai==1.57.3

mlflow==3.7.0
