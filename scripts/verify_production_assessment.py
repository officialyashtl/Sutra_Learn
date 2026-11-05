import httpx
import time
import json
import uuid

BACKEND_URL = "https://sutra-learn-api.onrender.com"
FRONTEND_URL = "https://sutralearn.vercel.app"

client = httpx.Client(timeout=60.0)

print(f"[{time.strftime('%H:%M:%S')}] Polling Render production for assessment deployment...")

for attempt in range(1, 20):
    try:
        # Check health
        h = client.get(f"{BACKEND_URL}/api/v1/health")
        if h.status_code != 200:
            print(f"  Attempt {attempt}: Backend not healthy yet ({h.status_code})")
            time.sleep(10)
            continue

        # Authenticate
        login = client.post(f"{BACKEND_URL}/api/v1/auth/session", json={"learner_id": "student-01"})
        if login.status_code != 200:
            print(f"  Attempt {attempt}: Auth session returned {login.status_code}")
            time.sleep(10)
            continue

        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # Probe the new endpoint
        session_id = f"sess-prod-{uuid.uuid4().hex[:8]}"
        payload = {
            "concept_id": "MATH-C01",
            "session_id": session_id,
            "submissions": [
                {"question_id": "Q-INT-001", "selected_option_id": "A"},
                {"question_id": "Q-INT-002", "selected_option_id": "C"},
                {"question_id": "Q-INT-003", "selected_option_id": "A"},
                {"question_id": "Q-INT-004", "selected_option_id": "A"},
                {"question_id": "Q-INT-005", "selected_option_id": "A"},
            ]
        }
        res = client.post(f"{BACKEND_URL}/api/v1/assessments/complete", headers=headers, json=payload)
        
        if res.status_code == 200:
            data = res.json()
            print("\n>>> SUCCESS! New Assessment Engine is LIVE on Render! <<<")
            print(f"Score:       {data['score']}/{data['total_questions']} ({data['percentage']}%)")
            print(f"Passed:      {data['passed']}")
            print(f"Outcome:     {data['outcome']}")
            print(f"Next Lesson: {data['next_concept_id']} - {data['next_concept_title']} (Can Advance: {data['can_advance']})")
            ai_g = data.get("ai_guidance") or {}
            print(f"AI Provider: {ai_g.get('provider')} (Fallback: {ai_g.get('is_fallback')})")
            print(f"AI Summary:  {ai_g.get('summary')}")
            print(f"Strengths:   {ai_g.get('strengths')}")
            print(f"Focus Area:  {ai_g.get('focus_area')}")
            print(f"Action Step: {ai_g.get('action_step')}")
            break
        elif res.status_code == 404:
            print(f"  Attempt {attempt} at {time.strftime('%H:%M:%S')}: 404 Not Found (old build still running, waiting for Render deploy...)")
        else:
            print(f"  Attempt {attempt} at {time.strftime('%H:%M:%S')}: Status {res.status_code}: {res.text[:150]}")
    except Exception as e:
        print(f"  Attempt {attempt} Exception: {e}")

    time.sleep(15)

# Verify Vercel frontend
try:
    f_res = client.get(FRONTEND_URL)
    print(f"\nVercel Frontend Status: {f_res.status_code}")
except Exception as e:
    print(f"\nVercel Frontend Check Error: {e}")

