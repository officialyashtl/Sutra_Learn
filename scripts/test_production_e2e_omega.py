#!/usr/bin/env python3
"""
SUTRA LEARN — Production End-to-End Live Verification Suite
Executes end-to-end tests against:
- Hosted Frontend: https://sutralearn.vercel.app
- Hosted Backend:  https://sutra-learn-api.onrender.com

Tests:
1. Vercel Frontend asset delivery, SPA routing, bundle configuration
2. Backend API health & Gemini configuration status
3. Authentication (Login & Session issuance)
4. Session Creation (POST /api/v1/tutor/sessions)
5. Live Gemini Tutor Inference across ALL SIX Modes:
   - socratic (Guided Learning)
   - worked_example (Worked Example)
   - practice (Practice Question)
   - check_work (Check My Work)
   - revision (Quick Revision)
   - prerequisites (Prerequisites)
6. Message Persistence & History Retrieval (GET /api/v1/tutor/sessions/{id})
7. Session Reset / Clear & Restart (POST /api/v1/tutor/sessions/{id}/reset)
8. Multi-Tenant Tenancy Isolation (Learner B accessing Learner A -> 403)
9. Error-Free API Routing (0 unexpected 401, 404, 500, or CORS failures)
"""

import sys
import time
import json
import uuid
import httpx
from datetime import datetime, timezone

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BACKEND_URL = "https://sutra-learn-api.onrender.com"
FRONTEND_URL = "https://sutralearn.vercel.app"

TUTOR_MODES = [
    ("socratic", "Guided Learning", "How do I balance 3x - 7 = 14 step by step?"),
    ("worked_example", "Worked Example", "Show me a complete annotated solution for solving 5y + 10 = 35."),
    ("practice", "Practice Question", "Give me a practice problem about linear equations with one variable."),
    ("check_work", "Check My Work", "I solved 4x = 24 and got x = 8. Where did I make a mistake?"),
    ("revision", "Quick Revision", "Summarize the essential rules for transposing terms across the equals sign."),
    ("prerequisites", "Prerequisites", "What basic arithmetic concepts do I need before learning linear equations?")
]

results = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "backend_url": BACKEND_URL,
    "frontend_url": FRONTEND_URL,
    "git_commit": "b5799ba",
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "checks": {},
    "tutor_modes_tested": {},
    "gemini_inference_samples": [],
    "all_passed": False
}

def record_check(name: str, passed: bool, detail: any):
    results["checks"][name] = {
        "status": "PASS" if passed else "FAIL",
        "detail": detail
    }
    symbol = "PASS" if passed else "FAIL"
    print(f"[{symbol}] {name}: {'PASS' if passed else 'FAIL'}")
    if not passed:
        print(f"    Detail: {detail}")

def main():
    print("=" * 80)
    print("SUTRA LEARN — HOSTED PRODUCTION END-TO-END TEST SUITE")
    print(f"Backend Target:  {BACKEND_URL}")
    print(f"Frontend Target: {FRONTEND_URL}")
    print("=" * 80)

    client = httpx.Client(timeout=60.0)

    # -------------------------------------------------------------------------
    # 1. FRONTEND VERIFICATION (Vercel)
    # -------------------------------------------------------------------------
    print("\n--- 1. Testing Vercel Hosted Frontend ---")
    try:
        results["total_requests"] += 1
        resp = client.get(FRONTEND_URL)
        if resp.status_code == 200:
            results["successful_requests"] += 1
            has_root = '<div id="root">' in resp.text
            has_bundle = "/assets/index-" in resp.text
            record_check("vercel_index_html", has_root and has_bundle, {
                "status_code": resp.status_code,
                "has_root_div": has_root,
                "has_asset_bundle": has_bundle
            })
        else:
            results["failed_requests"] += 1
            record_check("vercel_index_html", False, f"Status: {resp.status_code}")
    except Exception as e:
        results["failed_requests"] += 1
        record_check("vercel_index_html", False, str(e))

    # Test SPA rewrite route on Vercel
    try:
        results["total_requests"] += 1
        spa_resp = client.get(f"{FRONTEND_URL}/student/tutor")
        if spa_resp.status_code == 200 and '<div id="root">' in spa_resp.text:
            results["successful_requests"] += 1
            record_check("vercel_spa_routing", True, "SPA route /student/tutor returns 200 index.html")
        else:
            results["failed_requests"] += 1
            record_check("vercel_spa_routing", False, f"Status: {spa_resp.status_code}")
    except Exception as e:
        results["failed_requests"] += 1
        record_check("vercel_spa_routing", False, str(e))

    # -------------------------------------------------------------------------
    # 2. BACKEND HEALTH & GEMINI STATUS (Render)
    # -------------------------------------------------------------------------
    print("\n--- 2. Testing Render Hosted Backend Health ---")
    try:
        results["total_requests"] += 1
        r_health = client.get(f"{BACKEND_URL}/api/v1/health")
        if r_health.status_code == 200:
            results["successful_requests"] += 1
            health_json = r_health.json()
            is_wal = health_json.get("database_mode") == "wal"
            record_check("render_backend_health", is_wal, health_json)
        else:
            results["failed_requests"] += 1
            record_check("render_backend_health", False, f"Status: {r_health.status_code}")
    except Exception as e:
        results["failed_requests"] += 1
        record_check("render_backend_health", False, str(e))

    try:
        results["total_requests"] += 1
        r_ai = client.get(f"{BACKEND_URL}/api/v1/ai/health")
        if r_ai.status_code == 200:
            results["successful_requests"] += 1
            ai_data = r_ai.json()
            gemini_prov = next((p for p in ai_data.get("providers", []) if p.get("provider_id") == "gemini"), None)
            is_gemini_ok = (
                gemini_prov is not None
                and gemini_prov.get("configured") is True
                and gemini_prov.get("enabled") is True
                and gemini_prov.get("health_status") == "AVAILABLE"
                and gemini_prov.get("model_id") == "gemini-flash-lite-latest"
            )
            record_check("render_gemini_configured", is_gemini_ok, {
                "operating_mode": ai_data.get("operating_mode"),
                "gemini_provider": gemini_prov
            })
        else:
            results["failed_requests"] += 1
            record_check("render_gemini_configured", False, f"Status: {r_ai.status_code}")
    except Exception as e:
        results["failed_requests"] += 1
        record_check("render_gemini_configured", False, str(e))

    # -------------------------------------------------------------------------
    # 3. AUTHENTICATION & SESSION ISSUANCE
    # -------------------------------------------------------------------------
    print("\n--- 3. Testing Authentication & Token Issuance ---")
    student_a_token = None
    try:
        results["total_requests"] += 1
        login_resp = client.post(
            f"{BACKEND_URL}/api/v1/auth/login",
            json={"identifier": "student-01", "password": "sutra123"}
        )
        if login_resp.status_code == 200:
            results["successful_requests"] += 1
            token_data = login_resp.json()
            student_a_token = token_data.get("access_token")
            record_check("auth_login_student", bool(student_a_token), {
                "user_id": token_data.get("user_id"),
                "name": token_data.get("name"),
                "role": token_data.get("role"),
                "redirect_to": token_data.get("redirect_to")
            })
        else:
            results["failed_requests"] += 1
            record_check("auth_login_student", False, f"Status: {login_resp.status_code}, Body: {login_resp.text}")
    except Exception as e:
        results["failed_requests"] += 1
        record_check("auth_login_student", False, str(e))

    if not student_a_token:
        print("[CRITICAL] Could not obtain authentication token. Halting test suite.")
        sys.exit(1)

    headers_a = {
        "Authorization": f"Bearer {student_a_token}",
        "Content-Type": "application/json"
    }

    # -------------------------------------------------------------------------
    # 4. CONVERSATION SESSION CREATION (POST /api/v1/tutor/sessions)
    # -------------------------------------------------------------------------
    print("\n--- 4. Testing Dedicated Session Creation ---")
    session_id = None
    try:
        results["total_requests"] += 1
        create_resp = client.post(
            f"{BACKEND_URL}/api/v1/tutor/sessions",
            headers=headers_a,
            json={"concept_id": "MATH-C01", "title": "Production E2E Session"}
        )
        if create_resp.status_code in (200, 201):
            results["successful_requests"] += 1
            sess_data = create_resp.json()
            session_id = sess_data.get("id")
            record_check("tutor_session_creation", bool(session_id), sess_data)
        else:
            results["failed_requests"] += 1
            record_check("tutor_session_creation", False, f"Status: {create_resp.status_code}, Body: {create_resp.text}")
    except Exception as e:
        results["failed_requests"] += 1
        record_check("tutor_session_creation", False, str(e))

    # Fallback to UUID if creation had an unexpected response format
    if not session_id:
        session_id = str(uuid.uuid4())

    # -------------------------------------------------------------------------
    # 5. LIVE GEMINI INFERENCE ACROSS ALL 6 MODES
    # -------------------------------------------------------------------------
    print("\n--- 5. Testing Live Gemini Inference Across All 6 Modes ---")
    all_modes_ok = True

    for mode_id, mode_label, prompt_text in TUTOR_MODES:
        print(f"\n>> Invoking Mode: {mode_label} ({mode_id})...")
        t0 = time.time()
        try:
            results["total_requests"] += 1
            chat_resp = client.post(
                f"{BACKEND_URL}/api/v1/tutor/chat",
                headers=headers_a,
                json={
                    "message": prompt_text,
                    "concept_id": "MATH-C01",
                    "mode": mode_id,
                    "conversation_id": session_id
                },
                timeout=120.0
            )
            duration_ms = round((time.time() - t0) * 1000, 2)
            if chat_resp.status_code == 200:
                chat_data = chat_resp.json()
                prov_meta = chat_data.get("provider_metadata") or {}
                prov_name = prov_meta.get("provider") or chat_data.get("provider") or "Unknown"
                is_fallback = prov_meta.get("is_fallback", False)
                
                # If Google hit transient 503 high demand spike, retry once after brief pause
                if is_fallback or prov_name != "Google Gemini":
                    time.sleep(3.0)
                    results["total_requests"] += 1
                    t0_retry = time.time()
                    retry_resp = client.post(
                        f"{BACKEND_URL}/api/v1/tutor/chat",
                        headers=headers_a,
                        json={
                            "message": prompt_text,
                            "concept_id": "MATH-C01",
                            "mode": mode_id,
                            "conversation_id": session_id
                        },
                        timeout=120.0
                    )
                    if retry_resp.status_code == 200:
                        chat_resp = retry_resp
                        chat_data = chat_resp.json()
                        duration_ms = round((time.time() - t0_retry) * 1000, 2)
                        prov_meta = chat_data.get("provider_metadata") or {}
                        prov_name = prov_meta.get("provider") or chat_data.get("provider") or "Unknown"
                        is_fallback = prov_meta.get("is_fallback", False)

                results["successful_requests"] += 1
                explanation = chat_data.get("answer") or chat_data.get("explanation") or chat_data.get("response") or ""
                model_used = prov_meta.get("model") or chat_data.get("model") or "Unknown"
                
                is_valid_resp = len(explanation) > 50 and not is_fallback and prov_name == "Google Gemini"
                results["tutor_modes_tested"][mode_id] = {
                    "mode_label": mode_label,
                    "duration_ms": duration_ms,
                    "provider": prov_name,
                    "model": model_used,
                    "explanation_length": len(explanation),
                    "hints_count": len(chat_data.get("hints", [])),
                    "success": is_valid_resp
                }
                results["gemini_inference_samples"].append({
                    "mode": mode_id,
                    "duration_ms": duration_ms,
                    "provider": prov_name,
                    "model": model_used,
                    "snippet": explanation[:140] + "..."
                })
                print(f"   [{'PASS' if is_valid_resp else 'FAIL'}] {mode_label} returned {len(explanation)} chars in {duration_ms}ms (Provider: {prov_name}, Model: {model_used})")
                if not is_valid_resp:
                    all_modes_ok = False
            else:
                results["failed_requests"] += 1
                all_modes_ok = False
                results["tutor_modes_tested"][mode_id] = {
                    "mode_label": mode_label,
                    "status_code": chat_resp.status_code,
                    "error": chat_resp.text,
                    "success": False
                }
                print(f"   [FAIL] HTTP {chat_resp.status_code}: {chat_resp.text}")
        except Exception as e:
            results["failed_requests"] += 1
            all_modes_ok = False
            results["tutor_modes_tested"][mode_id] = {
                "mode_label": mode_label,
                "error": str(e),
                "success": False
            }
            print(f"   [FAIL] Exception: {e}")

    record_check("all_six_tutor_modes_gemini", all_modes_ok, results["tutor_modes_tested"])

    # -------------------------------------------------------------------------
    # 6. MESSAGE PERSISTENCE & HISTORY RETRIEVAL
    # -------------------------------------------------------------------------
    print("\n--- 6. Testing Message Persistence & Conversation Detail ---")
    try:
        results["total_requests"] += 1
        detail_resp = client.get(
            f"{BACKEND_URL}/api/v1/tutor/sessions/{session_id}",
            headers=headers_a
        )
        if detail_resp.status_code == 200:
            results["successful_requests"] += 1
            detail_data = detail_resp.json()
            msgs = detail_data.get("messages", [])
            # We ran 6 prompts, each generates 1 user + 1 assistant = 12 messages minimum
            has_persisted_msgs = len(msgs) >= 12
            record_check("session_messages_persistence", has_persisted_msgs, {
                "session_id": session_id,
                "message_count": len(msgs),
                "title": detail_data.get("title")
            })
        else:
            results["failed_requests"] += 1
            record_check("session_messages_persistence", False, f"Status: {detail_resp.status_code}")
    except Exception as e:
        results["failed_requests"] += 1
        record_check("session_messages_persistence", False, str(e))

    # Check conversation list retrieval
    try:
        results["total_requests"] += 1
        list_resp = client.get(
            f"{BACKEND_URL}/api/v1/tutor/sessions",
            headers=headers_a
        )
        if list_resp.status_code == 200:
            results["successful_requests"] += 1
            sessions_list = list_resp.json()
            target_found = any(s.get("id") == session_id for s in sessions_list)
            record_check("session_list_retrieval", target_found, {
                "total_sessions_count": len(sessions_list),
                "new_session_present": target_found
            })
        else:
            results["failed_requests"] += 1
            record_check("session_list_retrieval", False, f"Status: {list_resp.status_code}")
    except Exception as e:
        results["failed_requests"] += 1
        record_check("session_list_retrieval", False, str(e))

    # -------------------------------------------------------------------------
    # 7. CLEAR & RESTART / RESET SESSION (POST /sessions/{id}/reset)
    # -------------------------------------------------------------------------
    print("\n--- 7. Testing Non-Destructive Clear & Restart ---")
    try:
        results["total_requests"] += 1
        reset_resp = client.post(
            f"{BACKEND_URL}/api/v1/tutor/sessions/{session_id}/reset",
            headers=headers_a
        )
        if reset_resp.status_code == 200:
            results["successful_requests"] += 1
            reset_data = reset_resp.json()
            
            # Verify messages dropped to 0 while session container persists
            results["total_requests"] += 1
            verify_resp = client.get(
                f"{BACKEND_URL}/api/v1/tutor/sessions/{session_id}",
                headers=headers_a
            )
            if verify_resp.status_code == 200:
                results["successful_requests"] += 1
                cleared_detail = verify_resp.json()
                remaining_msgs = len(cleared_detail.get("messages", []))
                is_reset_ok = remaining_msgs == 0
                record_check("clear_and_restart_reset", is_reset_ok, {
                    "reset_response": reset_data,
                    "remaining_messages": remaining_msgs,
                    "container_preserved": True
                })
            else:
                results["failed_requests"] += 1
                record_check("clear_and_restart_reset", False, f"Verify status: {verify_resp.status_code}")
        else:
            results["failed_requests"] += 1
            record_check("clear_and_restart_reset", False, f"Reset status: {reset_resp.status_code}")
    except Exception as e:
        results["failed_requests"] += 1
        record_check("clear_and_restart_reset", False, str(e))

    # -------------------------------------------------------------------------
    # 8. MULTI-TENANT TENANCY ISOLATION (Learner B accessing Learner A)
    # -------------------------------------------------------------------------
    print("\n--- 8. Testing Multi-Tenant Learner Isolation ---")
    try:
        results["total_requests"] += 1
        login_b = client.post(
            f"{BACKEND_URL}/api/v1/auth/login",
            json={"identifier": "student-02", "password": "sutra123"}
        )
        if login_b.status_code == 200:
            results["successful_requests"] += 1
            token_b = login_b.json().get("access_token")
            headers_b = {"Authorization": f"Bearer {token_b}", "Content-Type": "application/json"}
            
            # Learner B attempts to inspect Learner A's session
            results["total_requests"] += 1
            probe_b = client.get(
                f"{BACKEND_URL}/api/v1/tutor/sessions/{session_id}",
                headers=headers_b
            )
            # Must return 403 Forbidden
            is_isolated = probe_b.status_code == 403
            record_check("multi_tenant_isolation_403", is_isolated, {
                "learner_b_probe_status": probe_b.status_code,
                "rejection_detail": probe_b.text
            })
            if probe_b.status_code == 403:
                results["successful_requests"] += 1
            else:
                results["failed_requests"] += 1
        else:
            results["failed_requests"] += 1
            record_check("multi_tenant_isolation_403", False, "Learner B login failed")
    except Exception as e:
        results["failed_requests"] += 1
        record_check("multi_tenant_isolation_403", False, str(e))

    # -------------------------------------------------------------------------
    # 9. SUMMARY & EVIDENCE PERSISTENCE
    # -------------------------------------------------------------------------
    all_passed = all(chk["status"] == "PASS" for chk in results["checks"].values())
    results["all_passed"] = all_passed

    print("\n" + "=" * 80)
    print("HOSTED PRODUCTION VERIFICATION SUMMARY")
    print(f"Total Requests Executed:      {results['total_requests']}")
    print(f"Successful Requests:          {results['successful_requests']}")
    print(f"Failed Requests:              {results['failed_requests']}")
    print(f"Overall Acceptance Status:    {'ALL PASS (100%)' if all_passed else 'SOME CHECKS FAILED'}")
    print("=" * 80)

    with open("docs/production_redeploy_evidence.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nEvidence written to docs/production_redeploy_evidence.json")
    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    main()
