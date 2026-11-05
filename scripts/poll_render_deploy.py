import httpx
import time

BACKEND_URL = "https://sutra-learn-api.onrender.com"
client = httpx.Client(timeout=120.0)

for attempt in range(1, 10):
    now_str = time.strftime("%H:%M:%S")
    print(f"Attempt {attempt} at {now_str}...")
    try:
        login = client.post(f"{BACKEND_URL}/api/v1/auth/login", json={"identifier": "student-01", "password": "sutra123"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        res = client.post(
            f"{BACKEND_URL}/api/v1/tutor/chat",
            headers=headers,
            json={
                "message": "I solved 4x = 24 and got x = 8. Where did I make a mistake?",
                "concept_id": "MATH-C01",
                "mode": "check_work"
            }
        )
        if res.status_code == 200:
            meta = res.json().get("provider_metadata") or {}
            prov = meta.get("provider")
            is_fb = meta.get("is_fallback")
            reason = meta.get("fallback_reason")
            print(f"  Result: Provider={prov}, is_fallback={is_fb}, reason={reason}")
            if not is_fb and prov == "Google Gemini":
                print(">>> NEW DEPLOYMENT IS LIVE! Google Gemini successfully verified on check_work!")
                break
    except Exception as e:
        print(f"  Exception: {e}")
    time.sleep(15)
