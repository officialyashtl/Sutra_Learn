"""
SUTRA LEARN — Deterministic Comprehensive End-to-End Verification Suite
Project Codename: SUTRA ASCENSION (Release Candidate 1.0)
Tests all architectural invariants, security boundaries, adaptive policies,
and AI intelligence systems against an isolated, self-cleaning test database.
"""

import sys
import os
import json
import time
import uuid
import sqlite3
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
TEST_DB_PATH = BACKEND_DIR / "test_e2e_isolated.db"
PYTHON_EXE = BACKEND_DIR / ".venv" / "Scripts" / "python.exe"
if not PYTHON_EXE.exists():
    PYTHON_EXE = Path(sys.executable)

TEST_PORT = 8005
API_BASE = f"http://127.0.0.1:{TEST_PORT}"


def request_json(url, method="GET", data=None, headers=None):
    """Executes an HTTP request and returns (status_code, response_json)."""
    if headers is None:
        headers = {}
    encoded_data = None
    if data is not None:
        encoded_data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5.0) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            err_json = json.loads(raw)
        except Exception:
            err_json = {"raw": raw}
        return e.code, err_json
    except Exception as e:
        return 0, {"error": str(e)}


all_passed = True


def check(stage_num: int, stage_name: str, condition: bool, detail: str = ""):
    global all_passed
    prefix = f"Stage {stage_num:02d} [{stage_name}]"
    if condition:
        print(f"  [PASS] {prefix} {detail}")
    else:
        print(f"  [FAIL] {prefix} {detail}")
        all_passed = False


def main():
    global all_passed
    print("=" * 80)
    print("SUTRA LEARN — COMPREHENSIVE E2E VERIFICATION SUITE")
    print(f"Isolated Test Database: {TEST_DB_PATH.name}")
    print(f"Target Server URL:     {API_BASE}")
    print("=" * 80)

    # 1. Clean previous test DB if any
    for p in [TEST_DB_PATH, Path(str(TEST_DB_PATH) + "-wal"), Path(str(TEST_DB_PATH) + "-shm")]:
        if p.exists():
            try:
                p.unlink()
            except Exception:
                pass

    # 2. Launch ephemeral backend server with isolated DB
    env = os.environ.copy()
    env["SUTRA_DB_PATH"] = str(TEST_DB_PATH)
    env["PYTHONPATH"] = str(BACKEND_DIR)
    env["APP_ENV"] = "testing"

    server_proc = subprocess.Popen(
        [
            str(PYTHON_EXE),
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(TEST_PORT),
            "--log-level",
            "warning",
        ],
        cwd=str(BACKEND_DIR),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        # Wait for server health
        server_ready = False
        health_body = {}
        for attempt in range(40):
            time.sleep(0.5)
            status, body = request_json(f"{API_BASE}/api/v1/health")
            if status == 200 and body.get("status") == "healthy":
                server_ready = True
                health_body = body
                break

        if not server_ready:
            print("CRITICAL: Server failed to start on test port.")
            server_proc.terminate()
            out, err = server_proc.communicate()
            print("Server stdout:", out.decode('utf-8', errors='ignore'))
            print("Server stderr:", err.decode('utf-8', errors='ignore'))
            sys.exit(1)

        # -------------------------------------------------------------------
        # Stage 01: Backend Health & WAL Mode
        # -------------------------------------------------------------------
        print("\n--- STAGE 01: BACKEND HEALTH & WAL JOURNALING ---")
        check(1, "Backend Health", health_body.get("status") == "healthy", f"status={health_body.get('status')}")
        check(1, "Database WAL Mode", health_body.get("database_mode") == "wal", f"mode={health_body.get('database_mode')}")

        # -------------------------------------------------------------------
        # Stage 02: Database Readiness & Schema Initialization
        # -------------------------------------------------------------------
        print("\n--- STAGE 02: DATABASE READINESS & SEED INTEGRITY ---")
        conn = sqlite3.connect(str(TEST_DB_PATH))
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM learners;")
        learner_count = cur.fetchone()[0]
        conn.close()
        check(2, "Database Readiness", learner_count >= 4, f"seeded_learners={learner_count}")

        # -------------------------------------------------------------------
        # Stage 03: Student Authentication & Cryptographic Token
        # -------------------------------------------------------------------
        print("\n--- STAGE 03: STUDENT AUTHENTICATION & TOKEN ISSUANCE ---")
        status, s_auth = request_json(f"{API_BASE}/api/v1/auth/session", method="POST", data={"learner_id": "student-01"})
        check(3, "Student Session Created", status == 200, f"status={status}")
        student_token = s_auth.get("access_token")
        check(3, "Bearer Token Present", bool(student_token) and student_token.startswith("sutra."))
        check(3, "Role is Student", s_auth.get("role") == "student")
        s_headers = {"Authorization": f"Bearer {student_token}"}

        # -------------------------------------------------------------------
        # Stage 04: Student Curriculum Access
        # -------------------------------------------------------------------
        print("\n--- STAGE 04: STUDENT CURRICULUM ACCESS ---")
        status, curr_data = request_json(f"{API_BASE}/api/v1/concepts", headers=s_headers)
        check(4, "Curriculum Retrieval", status == 200, f"status={status}")
        concepts = curr_data.get("concepts", [])
        check(4, "Curriculum Complete (30 NCERT Concepts)", len(concepts) == 30, f"count={len(concepts)}")

        # -------------------------------------------------------------------
        # Stage 05: Assessment Submission & Idempotent Retry Guarantee
        # -------------------------------------------------------------------
        print("\n--- STAGE 05: ASSESSMENT SUBMISSION & IDEMPOTENCY ---")
        test_attempt_id = f"e2e-attempt-{uuid.uuid4()}"
        attempt_payload = {
            "attempt_id": test_attempt_id,
            "learner_id": "student-01",
            "question_id": "Q-INT-001",
            "concept_id": "MATH-C01",
            "selected_option_id": "A",
            "hint_used": False,
        }
        status, att1 = request_json(f"{API_BASE}/api/v1/attempts", method="POST", data=attempt_payload, headers=s_headers)
        check(5, "First Attempt Submission", status == 200 and att1.get("is_duplicate") is False)

        status, att2 = request_json(f"{API_BASE}/api/v1/attempts", method="POST", data=attempt_payload, headers=s_headers)
        check(5, "Idempotent Re-submission", status == 200 and att2.get("is_duplicate") is True)

        # -------------------------------------------------------------------
        # Stage 06: Deterministic Adaptive Progression
        # -------------------------------------------------------------------
        print("\n--- STAGE 06: DETERMINISTIC ADAPTIVE EVALUATION ---")
        status, rec_data = request_json(
            f"{API_BASE}/api/v1/recommendations/evaluate",
            method="POST",
            data={"learner_id": "student-01", "concept_id": "MATH-C01"},
            headers=s_headers,
        )
        check(6, "Adaptive Recommendation Evaluated", status == 200, f"status={status}")
        valid_outcomes = {"BRIDGE_BACK", "SCAFFOLD", "STRETCH", "CONFIRM", "TEACHER_REVIEW"}
        outcome = rec_data.get("outcome")
        check(6, "Valid Pedagogical Outcome", outcome in valid_outcomes, f"outcome={outcome}")
        check(6, "Confidence Score Valid", 0.0 <= rec_data.get("confidence_score", -1.0) <= 1.0)

        # -------------------------------------------------------------------
        # Stage 07: Teacher Authentication & Verification
        # -------------------------------------------------------------------
        print("\n--- STAGE 07: TEACHER AUTHENTICATION & ROLE VERIFICATION ---")
        status, t_auth = request_json(f"{API_BASE}/api/v1/auth/session", method="POST", data={"learner_id": "teacher-01"})
        check(7, "Teacher Session Created", status == 200, f"status={status}")
        teacher_token = t_auth.get("access_token")
        check(7, "Teacher Role Enforced", t_auth.get("role") == "teacher")
        t_headers = {"Authorization": f"Bearer {teacher_token}"}

        # -------------------------------------------------------------------
        # Stage 08: Cohort Analytics & Accuracy Invariants (Accuracy <= 100%)
        # -------------------------------------------------------------------
        print("\n--- STAGE 08: COHORT ANALYTICS & ACCURACY INVARIANTS ---")
        status, cohort = request_json(f"{API_BASE}/api/v1/teacher/cohort", headers=t_headers)
        check(8, "Cohort Retrieval", status == 200, f"status={status}")
        check(8, "Cohort Size >= 3", len(cohort) >= 3, f"count={len(cohort)}")

        accuracy_invariants_hold = True
        for st in cohort:
            tot = st.get("total_attempts", 0)
            corr = st.get("total_correct", 0)
            acc = st.get("accuracy_percentage")
            if corr > tot or (acc is not None and acc > 100.0):
                accuracy_invariants_hold = False
        check(8, "Cohort Accuracy Invariant (<=100%)", accuracy_invariants_hold)

        # -------------------------------------------------------------------
        # Stage 09: Security Trust Boundaries (401 Missing, 403 Cross-Role)
        # -------------------------------------------------------------------
        print("\n--- STAGE 09: SECURITY TRUST BOUNDARIES & AUTHORIZATION ---")
        # 9A: Spoofed header without token -> 401
        status, _ = request_json(f"{API_BASE}/api/v1/teacher/cohort", headers={"x-teacher-id": "teacher-01"})
        check(9, "Spoofed Header Rejected (401)", status == 401, f"status={status}")

        # 9B: Student token calling teacher endpoint -> 403
        status, _ = request_json(f"{API_BASE}/api/v1/teacher/cohort", headers=s_headers)
        check(9, "Student Role Forbidden on Teacher Route (403)", status == 403, f"status={status}")

        # 9C: Tampered token -> 401
        status, _ = request_json(f"{API_BASE}/api/v1/teacher/cohort", headers={"Authorization": "Bearer sutra.fake.token"})
        check(9, "Tampered Token Rejected (401)", status == 401, f"status={status}")

        # -------------------------------------------------------------------
        # Stage 10: Cross-Student Resource Isolation
        # -------------------------------------------------------------------
        print("\n--- STAGE 10: CROSS-STUDENT RESOURCE ISOLATION ---")
        status, _ = request_json(f"{API_BASE}/api/v1/learners/student-02/progress", headers=s_headers)
        check(10, "Cross-Student Progress Blocked (403)", status == 403, f"status={status}")

        status, _ = request_json(f"{API_BASE}/api/v1/learners/student-02/attempts", headers=s_headers)
        check(10, "Cross-Student Attempts Blocked (403)", status == 403, f"status={status}")

        # Teacher CAN inspect learner attempts
        status, _ = request_json(f"{API_BASE}/api/v1/learners/student-02/attempts", headers=t_headers)
        check(10, "Teacher Authorized Inspection (200)", status == 200, f"status={status}")

        # -------------------------------------------------------------------
        # Stage 11: Teacher Clinical Interventions & Categorized Audit Trail
        # -------------------------------------------------------------------
        print("\n--- STAGE 11: TEACHER INTERVENTION & CATEGORIZED AUDIT ---")
        override_data = {
            "learner_id": "student-01",
            "concept_id": "MATH-C01",
            "previous_outcome": outcome or "CONFIRM",
            "overridden_outcome": "SCAFFOLD",
            "reason": "Pedagogical intervention: Targeted scaffold for sign rules.",
            "teacher_id": "teacher-01",
        }
        status, ov_res = request_json(f"{API_BASE}/api/v1/teacher/override", method="POST", data=override_data, headers=t_headers)
        check(11, "Teacher Override Applied", status == 200, f"status={status}")

        status, audit_events = request_json(
            f"{API_BASE}/api/v1/teacher/audit?category=PEDAGOGICAL_INTERVENTIONS",
            headers=t_headers,
        )
        check(11, "Categorized Audit Log Retrieval", status == 200 and len(audit_events) > 0)

        # -------------------------------------------------------------------
        # Stage 12: SUTRA AI Student Tutor & Conversation Privacy
        # -------------------------------------------------------------------
        print("\n--- STAGE 12: SUTRA AI TUTOR & CONVERSATION ISOLATION ---")
        tutor_req = {
            "message": "I do not understand how to solve 2x + 5 = 15",
            "concept_id": "MATH-C01",
            "mode": "guided_learning",
        }
        status, tutor_res = request_json(f"{API_BASE}/api/v1/tutor/chat", method="POST", data=tutor_req, headers=s_headers)
        check(12, "Tutor Chat Generates Response", status == 200, f"status={status}")
        conv_id = tutor_res.get("conversation_id")
        check(12, "Conversation ID Created", bool(conv_id))
        check(12, "Hints Provided", isinstance(tutor_res.get("hints"), list))

        # Cross-student conversation privacy check
        status, s2_auth = request_json(f"{API_BASE}/api/v1/auth/session", method="POST", data={"learner_id": "student-02"})
        s2_headers = {"Authorization": f"Bearer {s2_auth.get('access_token')}"}
        status, _ = request_json(f"{API_BASE}/api/v1/tutor/conversations/{conv_id}", headers=s2_headers)
        check(12, "Cross-Student Conversation Privacy (403)", status == 403, f"status={status}")

        # -------------------------------------------------------------------
        # Stage 13: SUTRA AI Educator Intelligence
        # -------------------------------------------------------------------
        print("\n--- STAGE 13: SUTRA AI EDUCATOR INTELLIGENCE ---")
        # Student calling educator assistant -> 403
        status, _ = request_json(
            f"{API_BASE}/api/v1/teacher/assistant/analyze",
            method="POST",
            data={"query": "Identify struggling students"},
            headers=s_headers,
        )
        check(13, "Student Blocked from Educator Assistant (403)", status == 403, f"status={status}")

        # Teacher calling educator assistant -> 200 with structured analysis
        status, ed_ai = request_json(
            f"{API_BASE}/api/v1/teacher/assistant/analyze",
            method="POST",
            data={"query": "Identify struggling students in linear equations"},
            headers=t_headers,
        )
        check(13, "Teacher Classroom Intelligence Generated", status == 200, f"status={status}")
        check(13, "Evidence Observations Present", len(ed_ai.get("observations", [])) > 0)
        check(13, "Actionable Recommendations Present", len(ed_ai.get("recommended_actions", [])) > 0)

        # -------------------------------------------------------------------
        # Stage 14: Data Integrity Verification Directly Against Database
        # -------------------------------------------------------------------
        print("\n--- STAGE 14: SQLITE DATABASE INVARIANTS & INTEGRITY ---")
        conn = sqlite3.connect(str(TEST_DB_PATH))
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM attempts WHERE is_correct NOT IN (0, 1);")
        invalid_correct = cur.fetchone()[0]
        check(14, "Boolean Invariant on Attempts", invalid_correct == 0)

        cur.execute("SELECT COUNT(*) FROM system_audit_logs;")
        audit_count = cur.fetchone()[0]
        check(14, "Audit Log Populated", audit_count > 0, f"audit_count={audit_count}")

        cur.execute("PRAGMA foreign_key_check;")
        fk_violations = cur.fetchall()
        check(14, "Zero Foreign Key Violations", len(fk_violations) == 0, f"violations={len(fk_violations)}")
        conn.close()

    finally:
        # Graceful shutdown of ephemeral server
        server_proc.terminate()
        try:
            server_proc.wait(timeout=3.0)
        except subprocess.TimeoutExpired:
            server_proc.kill()

        # Clean up isolated test DB files
        for p in [TEST_DB_PATH, Path(str(TEST_DB_PATH) + "-wal"), Path(str(TEST_DB_PATH) + "-shm")]:
            if p.exists():
                try:
                    p.unlink()
                except Exception:
                    pass

    # Final summary
    print("\n" + "=" * 80)
    if all_passed:
        print("ALL 14 E2E VERIFICATION STAGES PASSED SUCCESSFULLY (EXIT CODE 0)!")
        print("=" * 80)
        sys.exit(0)
    else:
        print("E2E VERIFICATION SUITE ENCOUNTERED FAILURES (EXIT CODE 1)!")
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    main()
