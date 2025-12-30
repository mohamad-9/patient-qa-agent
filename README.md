# 🩺 Patient Medical History Q&A Assistant (Non-Clinical)

---

## 📌 Project Overview

This project is a **non-clinical, healthcare-safe AI assistant**.

It allows users to ask **educational questions** related to their **own medical history, diagnoses, and symptoms**, and receive **simple explanations — without medical advice.**

⚠️ This system is **NOT a medical tool** and  
⚠️ **NOT a diagnostic system**

It is strictly for **learning + experimentation**.

---

## 🎯 Purpose of the Project

I built this project to learn:

✅ AI safety design  
✅ Medical-domain prompt control  
✅ FastAPI backend architecture  
✅ Docker deployment workflows  
✅ Cloud hosting  
✅ Safe logging with MLflow  

This version supports **chat-style conversation with context memory.**

---

## ✅ What the Assistant Can Do

✔ Explain **doctor-provided diagnoses**  
✔ Explain **medical terminology**  
✔ Explain **general mechanisms & symptoms**  
✔ Stay **educational & neutral**  
✔ Respect **healthcare AI safety boundaries**

---

## 🚫 What the Assistant Will NOT Do

The system will refuse to:

❌ Diagnose diseases  
❌ Recommend medications  
❌ Suggest treatments  
❌ Provide medical instructions  
❌ Replace a doctor  

If a question is unsafe → it responds with a **polite refusal**.

---

## 🧠 Safety Design (Layered)

Safety is enforced at multiple levels:

### 1️⃣ Frontend UI Guard
Users must provide either:

• medical history  
• diagnoses  
• symptoms  

(or toggle dev-mode for testing)

---

### 2️⃣ Backend Validation Guard
Empty / invalid requests are rejected

---

### 3️⃣ Safety Classifier
Blocks content like:

• diagnosis  
• medication advice  
• urgent warnings  
• prescriptive instructions  

---

### 4️⃣ Prompt Safety Rules
The AI is constrained to:

✔ educational language  
✔ neutral tone  
✔ no instructions  
✔ no clinical judgement  

---

### 5️⃣ Logging Safety
MLflow stores **only metadata** — never medical text.

---

## 🧪 Current Version

### Version: `v0.2 (Chat Upgrade Release)`

### New features
✨ Chat UI (conversation flow)  
✨ Multi-turn context memory  
✨ Safe prompt controls  
✨ UI polish  
✨ Local + cloud support  
✨ Docker deploy ready  

---

## 🌐 Live Deployment

The project is currently hosted online.

- **Demo UI**  
  https://patient-qa-agent-1.onrender.com/demo

- **API Documentation (Swagger)**  
  https://patient-qa-agent-1.onrender.com/docs

 - ** Health Check
   https://patient-qa-agent-1.onrender.com/health

 - **Auto-deploy:** Enabled on Render (deploys automatically on each git push to the    connected branch).


---

## 🛠 Tech Stack

- **Python 3.11**
- **FastAPI**
- **Uvicorn**
- **Hugging Face Inference API**
- **spaCy NLP**
- **MLflow (local file backend)**
- **Docker**
- **Render Cloud Hosting**

---

## 🔐 Environment Variables

Create a `.env` file:

HUGGINGFACE_API_TOKEN=hf_xxxxxxxxxxxxxxxxx

MLFLOW_TRACKING_URI=file:/app/mlruns

MLFLOW_EXPERIMENT_NAME=patient-qa-agent


---

## 📦 Python Dependencies
fastapi==0.115.5
uvicorn[standard]==0.32.0
pydantic==2.10.2
python-dotenv==1.0.1
requests==2.32.3
httpx==0.27.2
spacy==3.8.2
openai==1.57.3
mlflow==3.7.0

(The exact pinned versions are in `requirements.txt`.)

---

## ▶️ Local Development

### 1️⃣ Create venv

python -m venv .venv
source .venv/bin/activate


### 2️⃣ Install deps
pip install -r requirements.txt
python -m spacy download en_core_web_sm

### 3️⃣ Run API

uvicorn app.main:app --reload

Visit:
http://127.0.0.1:8000/demo


---

## 🐳 Docker (Recommended)

### Build
docker build -t patient-qa-agent:latest 

### Run
docker run --rm
-e HUGGINGFACE_API_TOKEN=YOUR_TOKEN
-p 8000:8000
patient-qa-agent:lates


Open:
http://localhost:8000/demo

---

## 🚀 Deploy to Render

Service type → **Web Service**  
Runtime → **Docker**  
Start command auto-handled by Dockerfile  

Environment variables must include:


---

## 🔎 Logging (Safe)

MLflow **does NOT store medical text**

It only logs:

✔ latency  
✔ counts of fields  
✔ model version  
✔ block status  

Stored locally in container at:


---

## ⚖️ Legal & Ethics Notice

This project is:

❌ NOT medical software  
❌ NOT certified  
❌ NOT treatment guidance  

Users must always consult a professional.

---

## 📌 Future Roadmap

- Conversation persistence
- Patient note summarization
- Multi-language UI
- Role-based safety improvements

---

## ❤️ Credits

Built for **learning AI safety in healthcare**.

Special thanks to:
- Hugging Face community
- FastAPI ecosystem

---

## 📄 License



---
