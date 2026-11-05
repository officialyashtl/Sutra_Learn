# SUTRA LEARN — Setup, Execution & Handover Guide
### Technical Onboarding & Local Reproduction Manual

This guide provides step-by-step instructions for running, testing, and verifying the complete **SUTRA LEARN** application from a fresh clone.

---

## 1. Prerequisites

- **Python:** Version 3.11.x installed and available in system PATH.
- **Node.js:** Version 18.x or 20.x LTS with `npm` (v9+).
- **Git:** Modern Git client.
- **Operating System:** Windows, macOS, or Linux.

---

## 2. Repository Layout

```
Sutra_Learn/
├── backend/
│   ├── app/
│   │   ├── ai/               # Gemini adapter, prompt shielding & assessment guidance
│   │   ├── content/          # NCERT 30 concepts & 81 diagnostic questions
│   │   ├── db/               # SQLite database setup, CRUD operations & migrations
│   │   ├── engine/           # Deterministic adaptive scoring state machine
│   │   ├── routers/          # FastAPI REST endpoints (/auth, /assessments, /tutor, etc.)
│   │   ├── services/         # Security auditing & trace logger
│   │   ├── auth.py           # JWT generation, PBKDF2 hashing & RBAC
│   │   ├── config.py         # Pydantic environment configuration
│   │   ├── main.py           # FastAPI ASGI entrypoint & middleware
│   │   └── schemas.py        # Pydantic API contract models
│   ├── tests/                # Automated pytest suite (46 passing tests)
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Template environment file
├── frontend/
│   ├── public/               # Static assets, robots.txt, sitemap.xml, sw.js
│   ├── src/                  # React 18 TypeScript source code
│   ├── package.json          # Frontend dependencies & npm scripts
│   ├── tsconfig.json         # TypeScript compiler configuration
│   └── vite.config.ts        # Vite build & proxy configuration
├── docs/                     # Comprehensive engineering & submission documentation
├── screenshots/              # 48 cross-device visual evidence captures
└── scripts/                  # Automated verification scripts
```

---

## 3. Local Installation & Startup

### Step 1: Backend Setup
```powershell
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
# Copy the template to .env (ensure GEMINI_API_KEY is provided if testing cloud AI)
copy .env.example .env

# 6. Start backend development server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
- **Backend API Health Check:** `http://127.0.0.1:8000/api/v1/health`
- **Swagger / OpenAPI Documentation:** `http://127.0.0.1:8000/docs`

### Step 2: Frontend Setup
```powershell
# 1. Open a new terminal and navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```
- Open your browser at: `http://localhost:5173`

---

## 4. Environment Variables Reference

| Variable | Target | Description | Example / Default |
| :--- | :--- | :--- | :--- |
| `APP_ENV` | Backend | Environment profile (`development`, `production`, `testing`) | `development` |
| `SECRET_KEY` | Backend | Cryptographic secret used for signing JWT tokens | `sutra_secret_development_key...` |
| `GEMINI_API_KEY` | Backend | Google Gemini API key for Socratic tutoring (Never exposed to client) | `AIzaSy...` |
| `DATABASE_URL` | Backend | SQLite connection string | `sqlite:///./sutra.db` |
| `AI_PROVIDER` | Backend | AI provider selection (`gemini` or `mock`) | `gemini` |
| `AI_ENABLE_GEMINI` | Backend | Boolean flag enabling cloud Gemini inference | `true` |
| `VITE_API_URL` | Frontend | Base URL of the backend API gateway | `http://127.0.0.1:8000` |

> [!CAUTION]
> Never commit actual API keys to version control. The client bundle is strictly isolated from `GEMINI_API_KEY`.

---

## 5. Verification & Testing Commands

### Backend Pytest Suite (46 Tests)
```powershell
python -m pytest backend/tests/
```

### Rectification & Edge-Case Matrix (10 Criteria)
```powershell
python scripts/verify_rectification_matrix.py
```

### Frontend Linter
```powershell
cd frontend
npm run lint
```

### Frontend Production Build
```powershell
cd frontend
npm run build
```

---

## 6. Seed Accounts & Credentials

The SQLite database seeds automatically on boot with the following verified test accounts:

| User | Role | Identifier | Password | Context |
| :--- | :--- | :--- | :--- | :--- |
| **Aarav Sharma** | Student | `student-01` | `sutra123` | First-time learner starting Integer Arithmetic (`MATH-C01`) |
| **Diya Patel** | Student | `student-02` | `sutra123` | Student demonstrating negative integer sign misconceptions |
| **Kabir Sen** | Student | `student-03` | `sutra123` | Advanced learner ready for multi-step equations |
| **Ms. Ananya Roy** | Teacher | `teacher-01` | `teacher123` | Mathematics Department Head with cohort oversight |

---

## 7. Troubleshooting & Common Questions

1. **Port 8000 Already in Use:**
   Run `uvicorn app.main:app --port 8001` and update `VITE_API_URL=http://127.0.0.1:8001` in `frontend/.env`.
2. **Backend Cold-Boot on Render:**
   When accessing `https://sutra-learn-api.onrender.com`, allow 30–50 seconds for free-tier instance wake-up if dormant.
3. **Database Reset (Local Development Only):**
   Delete `backend/sutra.db`. On next server restart, `init_db()` will automatically re-create all tables, foreign keys, and seed records.

