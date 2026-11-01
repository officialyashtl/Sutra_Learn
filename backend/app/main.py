from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import init_db, get_db_connection
from app.routers import curriculum, assessment, learners, teacher, auth, tutor, educator_assistant, ai


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:4173",
        "*"
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["*"],
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
