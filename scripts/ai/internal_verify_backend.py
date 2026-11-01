import sys
import json

sys.path.insert(0, "backend")
from fastapi.testclient import TestClient
from app.main import app
from app.auth import create_access_token

client = TestClient(app)

# 1. Health endpoint
res_h = client.get("/api/v1/ai/health")
assert res_h.status_code == 200, f"Health failed: {res_h.text}"
h_data = res_h.json()
assert h_data["status"] == "healthy"
assert "circuit_breakers" in h_data
assert len(h_data["providers"]) >= 4

# 2. Providers endpoint (Authenticated)
token = create_access_token("teacher-01", "teacher", "Ms. Ananya Roy")
res_p = client.get("/api/v1/ai/providers", headers={"Authorization": f"Bearer {token}"})
assert res_p.status_code == 200, f"Providers failed: {res_p.text}"
p_data = res_p.json()
assert len(p_data) >= 4

# 3. Tutor Orchestration endpoint (Authenticated)
s_token = create_access_token("student-01", "student", "Arjun Sharma")

from app.ai.orchestrator import get_ai_orchestrator
orc = get_ai_orchestrator()
# Set short timeouts for quick test execution
orc.settings.qwen_timeout_seconds = 2.0
orc.settings.gemma_timeout_seconds = 15.0

res_t = client.post(
    "/api/v1/ai/tutor",
    json={
        "message": "Explain why we add the same number to both sides of an equation.",
        "concept_id": "MATH-C01",
        "mode": "explain_concept"
    },
    headers={"Authorization": f"Bearer {s_token}"}
)
assert res_t.status_code == 200, f"Tutor failed: {res_t.text}"
t_data = res_t.json()
assert "request_id" in t_data
assert t_data["request_id"].startswith("req_")
assert "answer" in t_data
assert len(t_data["answer"]) > 20
assert t_data["validation_status"] in ("VERIFIED", "CURRICULUM_VERIFIED")

# 4. Educator Orchestration endpoint (Authenticated + Role-guarded)
# 4a. Student forbidden
res_e_forbidden = client.post(
    "/api/v1/ai/educator",
    json={"query": "Analyze classroom performance"},
    headers={"Authorization": f"Bearer {s_token}"}
)
assert res_e_forbidden.status_code == 403, f"Student should be forbidden: {res_e_forbidden.status_code}"

# 4b. Teacher allowed
res_e = client.post(
    "/api/v1/ai/educator",
    json={"query": "Analyze linear equations friction points and suggest interventions"},
    headers={"Authorization": f"Bearer {token}"}
)
assert res_e.status_code == 200, f"Educator endpoint failed: {res_e.text}"
e_data = res_e.json()
assert "summary" in e_data
assert "observations" in e_data
assert "recommended_actions" in e_data

print(json.dumps({
    "status": "SUCCESS",
    "providers_count": len(p_data),
    "request_id": t_data["request_id"],
    "selected_provider": t_data["provider"],
    "selected_model": t_data["model"],
    "validation_status": t_data["validation_status"],
    "educator_verified": True,
    "latency_ms": t_data["latency_ms"]
}))
