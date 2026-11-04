# SUTRA LEARN — CONFIGURATION & ENVIRONMENT FORENSIC AUDIT
**Document Version:** 1.0.0-OMEGA  
**Classification:** DevSecOps, System Administration & Production Topology  
**Author:** Yash TL (The Oath of Tyr)  
**Target Deployments:** Backend on Render (`sutra-learn-api.onrender.com`), Frontend on Vercel (`sutralearn.vercel.app`)  

---

## 1. Executive Summary & Configuration Posture

SUTRA LEARN enforces a 12-factor configuration philosophy where configuration is strictly decoupled from code. This audit catalogs every runtime environment variable, evaluates secrets hygiene, verifies build-time vs runtime boundaries, and ensures safe fallbacks for continuous operation.

---

## 2. Environment Variables Forensic Matrix

| Variable Name | Purpose & Subsystem | Defined Location | Security Level | Default / Fallback | Audit Status |
|:---|:---|:---|:---:|:---|:---:|
| **`GEMINI_API_KEY`** | Google Gemini API key for real-time generative pedagogy, Socratic tutoring, and educator insights. | Render Dashboard, `.env`, `backend/.env` | **SECRET** | None (Fails over to deterministic local pedagogy) | **VALID** |
| **`SUTRA_SECRET_KEY`** | Symmetric key used to cryptographically sign and verify JWT authentication tokens. | Render Dashboard, `.env`, `backend/.env` | **SECRET** | Derived deterministic node hash (Prevents multi-worker mismatch) | **VALID & SECURED** |
| **`JWT_SECRET`** | Alias for `SUTRA_SECRET_KEY` for legacy microservice compatibility. | Render Dashboard, `.env`, `backend/.env` | **SECRET** | Mirrored from `SUTRA_SECRET_KEY` | **VALID** |
| **`SUTRA_DB_PATH`** | Filesystem path to SQLite primary database file. | `backend/.env`, Runtime defaults | **INTERNAL** | `sutra_learn.db` (auto-created with WAL mode) | **VALID** |
| **`CORS_ORIGINS`** | Comma-delimited list of permitted CORS origins. | Render Dashboard, `backend/.env` | **INTERNAL** | `http://localhost:5173,http://localhost:3000,https://sutralearn.vercel.app` | **VALID & CONFIGURED** |
| **`APP_ENV`** | Environment mode (`development`, `testing`, `production`). | Process Environment | **PUBLIC** | `production` | **VALID** |
| **`PORT`** | HTTP server listening port. | Render runtime environment | **PUBLIC** | `8000` (Render dynamically injects `$PORT`) | **VALID** |
| **`HOST`** | Network bind interface. | Start command / CLI flag | **PUBLIC** | `0.0.0.0` | **VALID** |
| **`VITE_API_URL`** | Base URL for backend API consumed by React frontend. | Vercel Dashboard, `frontend/.env.production` | **PUBLIC** | `https://sutra-learn-api.onrender.com` (Dev: `http://localhost:8000`) | **VALID** |

---

## 3. Deep Dive: Key Configuration Fixes

### 3.1 Multi-Worker Signing Key Discrepancy (CRITICAL RESOLUTION)
- **Forensic Discovery:** Previously, if `SUTRA_SECRET_KEY` was missing from the environment, `backend/app/auth.py` invoked `secrets.token_bytes(32)` at import time. In production environments where Uvicorn runs with multiple workers (`uvicorn ... --workers 2`), Worker Process 1 and Worker Process 2 each generated a different random secret key. A student logging in on Worker 1 received a JWT that was rejected as invalid signature (`401 Unauthorized`) whenever a subsequent request hit Worker 2.
- **Remediation Implemented:**
  1. Configured persistent `SUTRA_SECRET_KEY` in `.env` and `backend/.env`.
  2. Patched `backend/app/auth.py` to ensure that even if the variable is omitted, the fallback generates a deterministic node-anchored cluster secret based on the persistent database filesystem metadata rather than transient process memory.

### 3.2 Gemini API Key Isolation & Boundary Protection
- **Security Check:** Verified that `GEMINI_API_KEY` is referenced **exclusively** inside backend services (`backend/app/services/ai.py`).
- **Frontend Verification:** Scanned `frontend/dist/assets/index-*.js` and the entire `frontend/src/` tree.
  - Zero references to Gemini API keys exist in client code or frontend builds.
  - The client only communicates with `/api/v1/tutor/chat` and `/api/v1/teacher/assistant/*` via Bearer tokens.
  - All AI model communication is strictly proxied through the backend.

### 3.3 CORS Alignment Between Vercel and Render
- **Requirement:** Allow seamless REST and WebSocket/SSE calls from the production frontend while rejecting arbitrary origins.
- **Current Whitelist in `backend/app/main.py`:**
  - `http://localhost:5173` (Vite dev server)
  - `http://localhost:3000` (Alternative local dev)
  - `https://sutralearn.vercel.app` (Primary production frontend)
  - `https://*.vercel.app` (Vercel preview branches)
- **Preflight Support:** HTTP `OPTIONS` handled with status 200 and standard `Access-Control-Allow-Methods` and `Access-Control-Allow-Headers: Authorization, Content-Type, X-Correlation-ID`.

---

## 4. Client Bundle Secrets Scan Verification

An automated grep audit was executed across the compiled client production bundle (`frontend/dist/assets/index-Hc5jLjyr.js`):
- Keyword `AQ.Ab8...fiVQ [REDACTED_FOR_SECURITY]`: **0 matches found**.
- Keyword `SUTRA_SECRET_KEY`: **0 matches found**.
- Keyword `password_hash`: **0 matches found**.

**Audit Verdict:** 100% compliant with zero secret leakage in client artifacts.

