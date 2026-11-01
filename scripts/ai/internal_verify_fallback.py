import sys
import json
import asyncio

sys.path.insert(0, "backend")
from app.ai.provider import CurriculumGroundedFallbackProvider
from app.ai.math_validator import MathematicalValidator

fallback = CurriculumGroundedFallbackProvider()

async def test_fallback():
    # 1. Worked example generation
    res_ex = await fallback.generate_tutor_response(
        message="Show me a worked example for linear equations",
        concept_id="MATH-C01",
        mode="worked_example",
        conversation_history=[],
        learner_context={}
    )
    assert res_ex["response_type"] == "worked_example"
    assert "Step 1" in res_ex["answer"]

    # 2. Mathematical validation
    val = MathematicalValidator.validate_step_consistency(res_ex["answer"])
    assert val["valid"] is True

    # 3. Guided explanation
    res_guide = await fallback.generate_tutor_response(
        message="Why do we transpose terms across the equals sign?",
        concept_id="MATH-C01",
        mode="guided_learning",
        conversation_history=[],
        learner_context={}
    )
    assert res_guide["response_type"] == "guided_explanation"
    assert len(res_guide["hints"]) > 0

    print(json.dumps({
        "status": "SUCCESS",
        "worked_example_steps_verified": val.get("verified_steps", 0),
        "validation_reason": val.get("reason"),
        "hints_count": len(res_guide["hints"])
    }))

asyncio.run(test_fallback())

