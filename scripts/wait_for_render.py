import httpx
import time
import sys

BACKEND_URL = "https://sutra-learn-api.onrender.com"
client = httpx.Client(timeout=30.0)

print(f"Monitoring Render backend at {BACKEND_URL}...")
start_time = time.time()

while time.time() - start_time < 240:
    try:
        r = client.get(f"{BACKEND_URL}/api/v1/health")
        if r.status_code == 200:
            print(f"[{time.strftime('%H:%M:%S')}] Health check: {r.status_code} - {r.json()}")
            break
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Waiting for service... ({e})")
    time.sleep(10)

print("Backend reachable.")
