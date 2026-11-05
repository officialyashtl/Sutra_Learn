"""
SUTRA LEARN — Live Production Non-Destructive Probe
Verifies deployed Render API and Vercel Frontend behavior without mutating production data.
"""

import urllib.request
import urllib.error
import ssl
import json

BASE_URL = "https://sutra-learn-api.onrender.com"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def make_req(path, method="GET", data=None, token=None):
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json", "User-Agent": "SutraLearn-Auditor/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=25) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(err_body)
        except Exception:
            return e.code, err_body
    except Exception as e:
        return 0, str(e)

print("=== SUTRA LEARN LIVE PRODUCTION AUDIT ===")

# 1. Health Probe
status, body = make_req("/api/v1/health")
print(f"1. Health Check (/api/v1/health): Status {status} -> {body}")

# 2. Concepts Probe
status, body = make_req("/api/v1/concepts")
if status == 200 and isinstance(body, dict):
    concept_list = body.get("concepts", [])
    print(f"2. Curriculum Concepts (/api/v1/concepts): Status 200 -> Count: {len(concept_list)} concepts loaded.")
    if concept_list:
        sample = concept_list[0]
        print(f"   Sample Concept: {sample.get('id')} - {sample.get('title')} (Grade {sample.get('grade')})")
else:
    print(f"2. Curriculum Concepts: Status {status} -> {body}")

# 3. Question Retrieval Probe
status, body = make_req("/api/v1/concepts/MATH-C01/questions")
if status == 200 and isinstance(body, list):
    print(f"3. Question Bank Retrieval (/api/v1/concepts/MATH-C01/questions): Status 200 -> Count: {len(body)} diagnostic items.")
    print(f"   Sample Question: {body[0].get('id')} - {body[0].get('prompt')}")
else:
    print(f"3. Question Bank Retrieval: Status {status} -> {body}")

# 4. Auth & Student Persona Check
status, body = make_req("/api/v1/auth/login", method="POST", data={"identifier": "student-01", "password": "sutra123"})
student_token = None
if status == 200 and "access_token" in body:
    student_token = body["access_token"]
    print(f"4. Student Authentication (student-01): Status 200 -> JWT Token Issued (User: {body.get('name')}, Role: {body.get('role')}).")
else:
    print(f"4. Student Authentication: Status {status} -> {body}")

# 5. Student Progress Retrieval
if student_token:
    status, body = make_req("/api/v1/learners/student-01/progress", token=student_token)
    concepts_progress = body.get("concepts", []) if isinstance(body, dict) else []
    print(f"5. Student Progress Retrieval (/learners/student-01/progress): Status {status} -> Progress records: {len(concepts_progress)}")

# 6. Student AI Past Conversations Retrieval
if student_token:
    status, body = make_req("/api/v1/tutor/conversations", token=student_token)
    print(f"6. Student AI Past Conversations (/tutor/conversations): Status {status} -> Total sessions: {len(body) if isinstance(body, list) else 'N/A'}")

# 7. Teacher Persona Check
status, body = make_req("/api/v1/auth/login", method="POST", data={"identifier": "teacher-01", "password": "teacher123"})
teacher_token = None
if status == 200 and "access_token" in body:
    teacher_token = body["access_token"]
    print(f"7. Teacher Authentication (teacher-01): Status 200 -> JWT Token Issued (User: {body.get('name')}, Role: {body.get('role')}).")
else:
    print(f"7. Teacher Authentication: Status {status} -> {body}")

# 8. Teacher Cohort Analytics
if teacher_token:
    status, body = make_req("/api/v1/teacher/cohort", token=teacher_token)
    print(f"8. Teacher Cohort Analytics (/teacher/cohort): Status {status} -> Active learners in cohort: {len(body) if isinstance(body, list) else 'N/A'}")

# 9. Educator Intelligence Insights
if teacher_token:
    status, body = make_req("/api/v1/teacher/assistant/insights", token=teacher_token)
    print(f"9. Educator Intelligence (/teacher/assistant/insights): Status {status} -> Total Learners: {body.get('total_learners') if isinstance(body, dict) else 'N/A'}")

# 10. Security Boundary Rejection: Student token on Teacher Endpoint
if student_token:
    status, body = make_req("/api/v1/teacher/cohort", token=student_token)
    print(f"10. Security Boundary (Student token on /teacher/cohort): Status {status} -> Forbidden: {status == 403}")

# 11. Security Boundary Rejection: Invalid Credentials
status, body = make_req("/api/v1/auth/login", method="POST", data={"identifier": "student-01", "password": "wrongpassword999"})
print(f"11. Security Boundary (Invalid Password): Status {status} -> Unauthorized: {status == 401}")

print("=== LIVE PRODUCTION AUDIT COMPLETE ===")
