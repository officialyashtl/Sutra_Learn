from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SUTRA LEARN API",
    description="Adaptive learning platform API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "sutra-learn-api",
        "version": "0.1.0",
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
        ],
    }
