import sys
import os
sys.path.insert(0, 'backend')

from app.db.database import init_db, get_db_connection
from app.db import crud
from app.schemas import AssessmentCompleteRequest, AssessmentSubmissionItem
from app.routers.assessment import complete_assessment, get_assessment_result_for_concept
from app.routers.curriculum import list_concepts
from starlette.requests import Request
import asyncio
import uuid

async def main():
    print("Initializing DB...")
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='assessment_results';")
    row = cursor.fetchone()
    print("Table assessment_results exists:", row[0] if row else "NO")
    conn.close()

    class MockRequest:
        state = type("State", (), {"correlation_id": "test-corr-123"})()
        headers = {}

    req_obj = MockRequest()
    student_user = {"id": "student-01", "role": "student", "name": "Aarav Sharma"}

    # Test 1: Submit a 100% correct assessment on MATH-C01 (all 5 items)
    conn = get_db_connection()
    fresh_session_id = f"sess-test-{uuid.uuid4().hex[:8]}"
    sub_req = AssessmentCompleteRequest(
        concept_id="MATH-C01",
        session_id=fresh_session_id,
        submissions=[
            AssessmentSubmissionItem(question_id="Q-INT-001", selected_option_id="A"),
            AssessmentSubmissionItem(question_id="Q-INT-002", selected_option_id="C"),
            AssessmentSubmissionItem(question_id="Q-INT-003", selected_option_id="A"),
            AssessmentSubmissionItem(question_id="Q-INT-004", selected_option_id="A"),
            AssessmentSubmissionItem(question_id="Q-INT-005", selected_option_id="A"),
        ]
    )
    result = await complete_assessment(sub_req, req_obj, student_user, conn)
    conn.close()

    print("\n--- Assessment 1 (100% Correct) Result ---")
    print(f"Score:       {result.score}/{result.total_questions} ({result.percentage}%)")
    print(f"Passed:      {result.passed}")
    print(f"Outcome:     {result.outcome}")
    print(f"Next Concept:{result.next_concept_id} - {result.next_concept_title} (Can Advance: {result.can_advance})")
    print(f"AI Guidance Provider: {result.ai_guidance.get('provider')} (Fallback: {result.ai_guidance.get('is_fallback')})")
    print(f"Summary:     {result.ai_guidance.get('summary')[:90]}...")
    print(f"Questions detailed: {len(result.questions_detail)}")

    # Test 2: Verify persistence retrieval
    conn = get_db_connection()
    persisted = get_assessment_result_for_concept("MATH-C01", student_user, conn)
    conn.close()
    print("\n--- Persisted Result Retrieval ---")
    print(f"Retrieved Result ID: {persisted.id}")
    print(f"Score: {persisted.score}/{persisted.total_questions}")
    print(f"Next Concept: {persisted.next_concept_id}")

    # Test 3: Verify list_concepts progression
    conn = get_db_connection()
    req_with_auth = MockRequest()
    concepts_out = list_concepts(req_with_auth, x_user_id="student-01", conn=conn)
    conn.close()
    
    math_c02 = next((c for c in concepts_out["concepts"] if c["id"] == "MATH-C02"), None)
    print("\n--- Next Lesson Progression Check ---")
    print(f"MATH-C02 is_unlocked: {math_c02.get('is_unlocked')} (Missing: {math_c02.get('missing_prerequisites')})")

    assert result.score == 5
    assert result.total_questions == 5
    assert result.passed is True
    assert result.can_advance is True
    assert result.next_concept_id == "MATH-C02"
    assert math_c02["is_unlocked"] is True
    print("\nALL BACKEND ACCEPTANCE CRITERIA PASSED!")

if __name__ == "__main__":
    asyncio.run(main())
