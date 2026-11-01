# SUTRA LEARN PHOENIX 10,000
## DOCUMENT 18: DEPLOYMENT OPERATIONS & RUNBOOK
**Version:** 1.0.0  
**Domain 19 (400 pts):** Deployment, Reliability & Operations  

---

### 1. Host Architecture & Prerequisites

- **OS:** Windows 11 (64-bit) / Ubuntu Linux 22.04 LTS
- **Python:** Python 3.11+
- **Node.js:** Node.js v18+ (npm v9+)
- **Ollama:** Version 0.5+ installed and listening on `127.0.0.1:11434`
- **Models Pulled:** `qwen3.5:4b` and `gemma4:e2b`

---

### 2. Step-by-Step Production Launch Sequence

#### Step 1: Initialize Ollama Daemon
```powershell
ollama serve
ollama list
# Confirm 'qwen3.5:4b' and 'gemma4:e2b' are present
```

#### Step 2: Configure Environment
Copy `.env.example` to `.env` and set environment variables:
```powershell
Copy-Item .env.example .env
```

#### Step 3: Start the Backend Service
```powershell
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --log-level info
```

#### Step 4: Build and Serve Frontend
```powershell
cd frontend
npm install
npm run build
npm run preview -- --port 5173
```

#### Step 5: Master Verification Run
```powershell
powershell -ExecutionPolicy Bypass -File scripts/ai/verify_ai_all.ps1
```

---

### 3. Graceful Shutdown & Disaster Recovery

- **Database Backup:** Because SQLite is running in WAL mode, taking a safe snapshot requires:
  ```powershell
  python -c "import sqlite3; con = sqlite3.connect('backend/sutra_learn.db'); bck = sqlite3.connect('backend/backup.db'); con.backup(bck); bck.close(); con.close()"
  ```
- **Service Termination:** Sending `SIGINT` (Ctrl+C) to uvicorn triggers graceful socket release and transaction flush without WAL file corruption.

