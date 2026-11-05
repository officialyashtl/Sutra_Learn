import httpx
import time
import json

BACKEND_URL = "https://sutra-learn-api.onrender.com"
client = httpx.Client(timeout=120.0)

# Login
login = client.post(f"{BACKEND_URL}/api/v1/auth/login", json={"identifier": "student-01", "password": "sutra123"})
token = login.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Test check_work mode with the exact prompt that previously triggered algebraic validator collision
prompt = "I solved 4x = 24 and got x = 8. Where did I make a mistake?"
print("Testing check_work prompt on Render...")
t0 = time.time()
res = client.post(
    f"{BACKEND_URL}/api/v1/tutor/chat",
    headers=headers,
    json={
        "message": prompt,
        "concept_id": "MATH-C01",
        "mode": "check_work"
    }
)
duration = round((time.time() - t0) * 1000, 2)
print(f"Status: {res.status_code} in {duration}ms")
if res.status_code == 200:
    data = res.json()
    meta = data.get("provider_metadata") or {}
    prov = meta.get("provider") or data.get("provider")
    model = meta.get("model") or data.get("model")
    is_fallback = meta.get("is_fallback")
    print(f"Provider:    {prov}")
    print(f"Model:       {model}")
    print(f"Is Fallback: {is_fallback}")
    print(f"Fallback Reason: {meta.get('fallback_reason')}")
    ans = data.get("answer", "")
    print(f"Answer snippet: {ans[:200]}...")
