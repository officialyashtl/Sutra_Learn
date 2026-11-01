# SUTRA LEARN — AI ASCENSION 1000
## DOCUMENT 19: DEPLOYMENT & PRODUCTION RUNBOOK
**Version:** 1.0.0  
**Target Environments:** Windows 11 / Linux Ubuntu / Containerized Docker  
**Runtime Components:** FastAPI Backend + React/Vite Frontend + Ollama Inference Runtime  

---

### 1. Prerequisites & Environment Setup

#### Python Environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

#### Node.js Environment:
```powershell
cd frontend
npm install
npm run build
```

#### Ollama Inference Setup:
Ensure the Ollama service is running and models are pulled:
```powershell
ollama pull qwen3.5:4b
ollama pull gemma4:e2b
ollama list
```

---

### 2. Environment Variables (`.env`)

```ini
# Application Configuration
APP_ENV=production
SUTRA_DB_PATH=backend/sutra_learn.db

# Multi-Model AI Configuration
AI_MODE=auto
AI_OFFLINE_MODE=false
GEMINI_API_KEY=(KEY)
GEMINI_MODEL=gemini-3.8-flash
GEMINI_TIMEOUT_SECONDS=15.0

# Ollama Local Configuration
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_QWEN_MODEL=qwen3.5:4b
OLLAMA_GEMMA_MODEL=gemma4:e2b
QWEN_TIMEOUT_SECONDS=45.0
GEMMA_TIMEOUT_SECONDS=20.0

# Resilience & Limits
AI_CIRCUIT_FAILURE_THRESHOLD=3
AI_CIRCUIT_COOLDOWN_SECONDS=60.0
AI_MAX_USER_INPUT_CHARS=8000
AI_MAX_HISTORY_MESSAGES=8
```

---

### 3. Production Service Launch

#### Launching the Backend:
```powershell
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Verification Command:
```powershell
powershell -ExecutionPolicy Bypass -File scripts/ai/verify_ai_backend.ps1
```
Expected output: `AI BACKEND PIPELINE VERIFICATION: SUCCESS (Exit Code 0)`.

