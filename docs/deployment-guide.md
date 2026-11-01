# SUTRA LEARN — Deployment & Operations Guide

## 1. Target Infrastructure Topology

SUTRA LEARN is architected for seamless cloud deployment:
- **Frontend SPA**: Hosted on **Vercel** or Netlify with global CDN distribution.
- **Backend API**: Hosted on **Render** (Web Service container) or AWS ECS / Google Cloud Run.
- **Database**: Embedded SQLite 3 in WAL mode (or Render Persistent Disk / AWS RDS PostgreSQL for enterprise scaling).

---

## 2. Environment Configuration

Create a production `.env` file based on `.env.example`:

```bash
# Server Runtime
PORT=8000
ENVIRONMENT=production
ALLOWED_ORIGINS=https://sutra-learn.vercel.app,https://sutra-learn.com

# Cryptography & Session Security
SUTRA_SECRET_KEY=generate-a-strong-random-hex-key-for-production
SESSION_EXPIRY_HOURS=24

# Persistence
SUTRA_DB_PATH=/var/data/sutra_learn.db

# Optional AI Intelligence (Gemini API)
# If omitted, platform seamlessly runs on deterministic Curriculum Fallback
GEMINI_API_KEY=AIzaSy...
```

---

## 3. Deployment to Render (Backend)

### Option A: `render.yaml` Blueprint

```yaml
services:
  - type: web
    name: sutra-learn-backend
    env: python
    region: oregon
    plan: starter
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    healthCheckPath: /api/v1/health
    disk:
      name: sutra-data
      mountPath: /var/data
      sizeGB: 10
    envVars:
      - key: SUTRA_DB_PATH
        value: /var/data/sutra_learn.db
      - key: SUTRA_SECRET_KEY
        generateValue: true
      - key: ALLOWED_ORIGINS
        value: "https://sutra-learn.vercel.app"
      - key: GEMINI_API_KEY
        sync: false
```

### Option B: Docker Container Deployment
Use the standardized `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
ENV SUTRA_DB_PATH=/data/sutra_learn.db
VOLUME ["/data"]

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 4. Deployment to Vercel (Frontend)

1. Connect the GitHub repository to Vercel.
2. Configure project settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
3. Configure Environment Variables:
   - `VITE_API_URL`: `https://sutra-learn-backend.onrender.com`
4. Deploy.

---

## 5. Health Checks & Verification Procedures

### Post-Deployment Liveness Check
```bash
curl -i https://sutra-learn-backend.onrender.com/api/v1/health
```
**Expected Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "database_mode": "wal",
  "version": "1.0.0"
}
```

### Smoke Test Sequence
1. Navigate to `https://sutra-learn.vercel.app/`.
2. Click "Student Portal" -> Log in as Aarav Sharma (`student-01`).
3. Verify Class 8 curriculum concepts load with demonstration status.
4. Open `/student/tutor` -> Send inquiry: "What is an inverse operation in algebra?"
5. Verify response renders cleanly with Socratic progressive hints.
6. Click "Sign Out".
7. Click "Educator Workspace" -> Log in as Ms. Ananya Roy (`teacher-01`).
8. Inspect cohort accuracy matrix and open `/teacher/assistant` for classroom synthesis.

---

## 6. Disaster Recovery & Rollback

- **SQLite Snapshot Backup**:
  ```bash
  sqlite3 /var/data/sutra_learn.db ".backup /var/data/backups/sutra_backup_$(date +%Y%m%d_%H%M%S).db"
  ```
- **Instant Rollback**: Render and Vercel support 1-click redeployment of previous immutable commit hashes.

