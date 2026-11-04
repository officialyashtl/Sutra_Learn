import os
import time
import uuid
import json
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Ensure environment variables are loaded immediately on application boot
load_dotenv(override=False)
load_dotenv("backend/.env", override=False)
load_dotenv("../.env", override=False)

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.database import init_db, get_db_connection
from app.routers import curriculum, assessment, learners, teacher, auth, tutor, educator_assistant, ai
from app.services.audit import record_audit_event, AuditCategory

logger = logging.getLogger("sutra.api.trace")


class APITraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Propagate or generate Correlation ID
        incoming_id = request.headers.get("X-Correlation-ID") or request.headers.get("X-Request-ID")
        correlation_id = incoming_id if incoming_id else f"req_{uuid.uuid4().hex[:12]}"
        request.state.correlation_id = correlation_id

        # 2. Extract origin and client IP
        client_ip = request.client.host if request.client else "unknown"
        origin = request.headers.get("origin") or request.headers.get("referer") or "direct"

        # 3. Inspect Authorization header safely
        auth_header = request.headers.get("Authorization")
        user_id = None
        user_role = None
        auth_outcome = "ANONYMOUS"
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1].strip()
            try:
                from app.auth import verify_access_token
                payload = verify_access_token(token)
                user_id = payload.get("sub")
                user_role = payload.get("role")
                auth_outcome = "AUTHENTICATED"
            except Exception:
                auth_outcome = "INVALID_TOKEN"

        # 4. Measure request duration
        start_time = time.perf_counter()
        error_category = None
        status_code = 500

        try:
            response: Response = await call_next(request)
            status_code = response.status_code
        except Exception as exc:
            error_category = type(exc).__name__
            status_code = 500
            raise exc
        finally:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            if status_code == 401:
                error_category = "UNAUTHORIZED"
            elif status_code == 403:
                error_category = "FORBIDDEN"
            elif status_code == 404:
                error_category = "NOT_FOUND"
            elif status_code == 422:
                error_category = "VALIDATION_ERROR"
            elif status_code == 429:
                error_category = "RATE_LIMITED"
            elif status_code >= 500:
                error_category = error_category or "SERVER_ERROR"

            trace_entry = {
                "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "client_ip": client_ip,
                "origin": origin,
                "user_id": user_id,
                "role": user_role,
                "auth_outcome": auth_outcome,
                "error_category": error_category
            }
            logger.info(f"API_TRACE: {json.dumps(trace_entry)}")

            # Record security rejections (401/403) and server errors (500) into system_audit_logs
            if status_code in (401, 403, 500) and not request.url.path.startswith("/docs") and not request.url.path.startswith("/openapi.json"):
                try:
                    conn = get_db_connection()
                    cat = AuditCategory.SECURITY if status_code in (401, 403) else AuditCategory.SYSTEM
                    record_audit_event(
                        conn=conn,
                        event_category=cat,
                        actor_id=user_id or "anonymous",
                        actor_role=user_role or "anonymous",
                        outcome="REJECTED" if status_code in (401, 403) else "FAILED",
                        rationale=f"HTTP {status_code} on {request.method} {request.url.path} ({error_category})",
                        correlation_id=correlation_id,
                        details={"ip": client_ip, "origin": origin, "auth_outcome": auth_outcome}
                    )
                    conn.close()
                except Exception:
                    pass

        response.headers["X-Correlation-ID"] = correlation_id
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database with foreign keys and seed records
    init_db()
    yield


app = FastAPI(
    title="SUTRA LEARN API",
    description="Adaptive learning platform API for Student Understanding, Targeted Reinforcement & Adaptation",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(APITraceMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:4173",
        "https://sutralearn.vercel.app",
        "*"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["X-Correlation-ID"]
)

# Mount feature routers
app.include_router(curriculum.router)
app.include_router(assessment.router)
app.include_router(learners.router)
app.include_router(teacher.router)
app.include_router(auth.router)
app.include_router(tutor.router)
app.include_router(educator_assistant.router)
app.include_router(ai.router)


@app.get("/api/v1/health")
def health_check():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode;")
        row = cursor.fetchone()
        journal_mode = row[0] if row else "unknown"
    finally:
        conn.close()
    return {
        "status": "healthy",
        "service": "sutra-learn-api",
        "version": "0.1.0",
        "database_mode": str(journal_mode).lower(),
    }


@app.get("/api/v1")
def api_info():
    return {
        "name": "SUTRA LEARN",
        "full_name": "Student Understanding, Targeted Reinforcement & Adaptation",
        "status": "development",
        "initial_scope": "Class 8 Mathematics - Linear Equations",
        "learning_paths": [
            "BRIDGE_BACK",
            "SCAFFOLD",
            "STRETCH",
            "CONFIRM",
            "TEACHER_REVIEW",
        ],
    }
