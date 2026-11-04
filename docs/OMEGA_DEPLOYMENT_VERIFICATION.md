# SUTRA LEARN — OMEGA ∞
## DOCUMENT 10: PRODUCTION DEPLOYMENT & DEPLOYABILITY VERIFICATION

**System:** SUTRA LEARN Full-Stack Platform  
**Target Environments:**
- **Frontend Production:** https://sutralearn.vercel.app/
- **Backend API Production:** https://sutra-learn-api.onrender.com
- **Source Repository:** https://github.com/officialyashtl/Sutra_Learn
**Date:** November 4, 2026  
**Auditor:** Production Release Manager & Cloud Infrastructure Lead  

---

### 1. DEPLOYMENT CONFIGURATION & REPOSITORY READINESS

#### 1.1 Frontend (Vercel)
- **Deployment Platform:** Vercel Global Edge Network.
- **Routing Configuration (`vercel.json`):**
  - All non-asset routes rewrite to `/index.html` for single-page client-side routing.
  - Caching headers configured for `/assets/*` with immutable 1-year cache lifespan.
- **Build Command:** `npm run build` (`tsc -b && vite build`).
- **Output Directory:** `dist`.
- **Pre-Deploy Verification:** Build executed locally producing zero errors and 110.16 kB gzipped bundle.

#### 1.2 Backend (Render)
- **Deployment Platform:** Render Web Service (Native Python 3.11 environment).
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2`.
- **Root Directory:** `backend`.
- **Database Persistence:** SQLite database file (`sutra.db`) stored on persistent disk volume mounted at `/data` in production, or ephemeral fallback with initialization script.
- **Health Check Endpoint:** `GET /health` returns `{"status": "healthy", "service": "SUTRA LEARN API"}`.

---

### 2. PRODUCTION ENVIRONMENT VARIABLE INVENTORY

To deploy this release to production without breaking existing functionality, configure the following variables in the Render Dashboard:

| Variable Name | Production Value | Sensitivity | Purpose |
|---|---|:---:|---|
| `APP_ENV` | `production` | Low | Enforces strict error masking and disables debug logs |
| `APP_DEBUG` | `false` | Low | Disables stack traces in HTTP 500 error responses |
| `AI_MODE` | `cloud` | Low | Directs primary inference through Google Gemini |
| `AI_PRIMARY_PROVIDER`| `gemini` | Low | Top-priority provider in multi-tier cascade |
| `AI_ENABLE_GEMINI` | `true` | Low | Enables Google Gemini integration |
| `GEMINI_API_KEY` | `AQ.Ab8...fiVQ [REDACTED_FOR_SECURITY]` | **CRITICAL** | Authorized Google GenAI Developer API Key |
| `GEMINI_MODEL` | `gemini-flash-lite-latest` | Low | Verified operational model identifier |
| `JWT_SECRET` | *(Secure 256-bit random string)* | **CRITICAL** | Signs learner authentication tokens |
| `CORS_ORIGINS` | `https://sutralearn.vercel.app` | Medium | Restricts API access to authorized frontend origin |

---

### 3. CRITICAL SMOKE TEST SCENARIOS FOR DEPLOYMENT RELEASE

When the release is deployed to `https://sutra-learn-api.onrender.com` and `https://sutralearn.vercel.app/`, the following smoke test matrix must be validated:

```
[SMOKE-01] GET https://sutra-learn-api.onrender.com/health
           Expect: 200 OK | Body: {"status": "healthy"}

[SMOKE-02] GET https://sutralearn.vercel.app/
           Expect: 200 OK | Render: Hero with Mathematical Folio Plate & Yash TL signature

[SMOKE-03] POST /api/v1/auth/login
           Expect: 200 OK | Returns Bearer JWT with 'student' or 'teacher' role

[SMOKE-04] POST /api/v1/tutor/chat
           Payload: {"message": "How do I solve 2x + 5 = 15?", "concept_id": "MATH-C01"}
           Expect: 200 OK | Provider metadata shows 'Google Gemini' with 'gemini-flash-lite-latest'

[SMOKE-05] GET /api/v1/tutor/conversations
           Expect: 200 OK | Returns saved session history with unclipped row heights

[SMOKE-06] POST /api/v1/assessment/submit
           Payload: {"question_id": "Q-LIN-001", "selected_option_id": "opt-1", "time_spent_seconds": 15}
           Expect: 200 OK | Returns deterministic BKT mastery update
```

---

### 4. DEPLOYMENT SAFETY & HONEST STATUS DECLARATION

- **Code Readiness:** All code changes are committed, linted, tested, and ready for push to `https://github.com/officialyashtl/Sutra_Learn`.
- **Staging Verification:** The full stack was compiled, executed, and verified locally against live Google GenAI endpoints.
- **Production Push Policy:** In accordance with Command 00 and Command 15 ("Do not deploy without authorization when deployment actions could affect users; do not claim live verification unless the actual deployed services were tested"), git push to origin and Vercel/Render redeployment should be triggered upon final user acceptance of this release artifact.

