# SUTRA LEARN — DEPLOYMENT & PRODUCTION OPERATIONS GUIDE
**Version:** 1.0.0 (Production Release)  
**Target Environments:** Render (Backend API) & Vercel (Frontend SPA)  

---

## 1. Production Architecture Overview

- **Backend API:** Hosted on Render (`https://sutra-learn-api.onrender.com`), running FastAPI with Uvicorn ASGI workers.
- **Frontend SPA:** Hosted on Vercel (`https://sutralearn.vercel.app`), serving compiled Vite/React static assets with client-side routing rewrites.
- **Continuous Deployment:** Connected to GitHub repository `https://github.com/officialyashtl/Sutra_Learn` on the `main` branch. Commits pushed to `main` trigger automated deployment pipelines across both platforms.

---

## 2. Backend Deployment Specification (Render)

### Service Configuration
- **Service Type:** Web Service
- **Environment:** Python 3.11
- **Root Directory:** Repository root (`.`)
- **Build Command:**
  ```bash
  pip install --upgrade pip && pip install -r backend/requirements.txt
  ```
- **Start Command:**
  ```bash
  cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2
  ```

### Required Environment Variables
| Variable Name | Required | Default / Example | Purpose |
| :--- | :---: | :--- | :--- |
| `APP_ENV` | Yes | `production` | Enables production security and strict audit logging |
| `PORT` | Auto | Provided by Render (`10000`) | Listening port for Uvicorn |
| `GEMINI_API_KEY` | Yes | `AIzaSy...` | Google GenAI API secret key for live inference |
| `GEMINI_MODEL` | Optional | `gemini-flash-lite-latest` | Preferred primary model identifier |
| `JWT_SECRET` | Yes | Strong 64-char hex secret | Cryptographic HMAC-SHA256 signing key |
| `SUTRA_DB_PATH` | Optional | `backend/sutra_learn.db` | Path to SQLite database file |

### Ephemeral Storage vs Persistent Disks
- **Free Tier Behavior:** In Render's free tier, local disk storage is ephemeral. Data resets during container rebuilds.
- **Persistent Disk Setup (Recommended for Long-Term Storage):**
  1. In the Render Dashboard, navigate to the `sutra-learn-api` service.
  2. Select **Disks** -> **Add Disk**.
  3. Mount path: `/var/data`, Size: 1 GB.
  4. Add environment variable: `SUTRA_DB_PATH=/var/data/sutra_learn.db`.

---

## 3. Frontend Deployment Specification (Vercel)

### Project Configuration
- **Framework Preset:** Vite
- **Root Directory:** `frontend`
- **Build Command:**
  ```bash
  npm run build
  ```
- **Output Directory:** `dist`
- **Install Command:**
  ```bash
  npm install
  ```

### Required Environment Variables
| Variable Name | Required | Value | Purpose |
| :--- | :---: | :--- | :--- |
| `VITE_API_URL` | Yes | `https://sutra-learn-api.onrender.com` | Production backend API target |

### Routing Rewrites (`vercel.json`)
To ensure deep client-side routes (e.g., `/student/home`, `/student/assessment/:id`, `/teacher/dashboard`) resolve properly upon browser reload without returning 404:
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

---

## 4. Local Development Reproduction

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm
- Valid Google Gemini API Key

### Step-by-Step Setup
```bash
# 1. Clone repository
git clone https://github.com/officialyashtl/Sutra_Learn.git
cd Sutra_Learn

# 2. Setup backend
cd backend
python -m venv venv
# Windows: venv\Scripts\activate | Unix: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your GEMINI_API_KEY and JWT_SECRET
uvicorn app.main:app --reload --port 8000

# 3. Setup frontend (in a separate terminal)
cd ../frontend
npm install
npm run dev
# Open http://localhost:5173
```
