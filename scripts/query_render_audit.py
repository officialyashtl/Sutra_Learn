import httpx
import json

client = httpx.Client(timeout=30)
login = client.post('https://sutra-learn-api.onrender.com/api/v1/auth/login', json={'identifier': 'teacher-01', 'password': 'teacher123'})
token = login.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

resp = client.get('https://sutra-learn-api.onrender.com/api/v1/teacher/audit?limit=15', headers=headers)
print('Audit Status:', resp.status_code)
logs = resp.json()
print(f'Total logs retrieved: {len(logs)}')
for log in logs[:15]:
    cat = log.get('event_category')
    actor = log.get('actor_id')
    rat = log.get('rationale')
    ts = log.get('created_at')
    print(f"[{ts}] {cat} | {actor} | {rat}")
    dt = log.get('details')
    if dt:
        try:
            parsed = json.loads(dt) if isinstance(dt, str) else dt
            print(f"   Details: {json.dumps(parsed)}")
        except Exception:
            print(f"   Details: {dt}")
