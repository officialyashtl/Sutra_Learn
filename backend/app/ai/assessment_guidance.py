"""
SUTRA LEARN — Assessment Guidance Generator
Generates personalized, Socratic pedagogical guidance for completed assessments.
Uses official Google GenAI SDK when configured, with high-quality NCERT curriculum
deterministic fallback.
"""

import os
import re
import json
import time
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from app.ai.config import get_ai_settings
from app.ai.gemini_adapter import GeminiAdapter
from app.content.concepts import get_concept

logger = logging.getLogger("sutra.ai.assessment_guidance")


def _generate_fallback_guidance(
    concept_title: str,
    score: int,
    total_questions: int,
    percentage: float,
    passed: bool,
    outcome: str,
    missed_questions: List[Dict[str, Any]],
    misconceptions: List[str],
    fallback_reason: Optional[str] = None
) -> Dict[str, Any]:
    """Generates deterministic NCERT curriculum-grounded guidance for completed assessments."""
    if percentage >= 100.0:
        summary = (
            f"Outstanding performance on {concept_title}! You answered all {total_questions} questions "
            f"correctly, demonstrating complete mathematical fluency and conceptual mastery."
        )
        strengths = [
            f"Rigorous application of core principles in {concept_title}.",
            "Clear procedural accuracy without relying on hints."
        ]
        focus_area = "Maintain this precision and step-by-step verification on more advanced, multi-step problems."
        action_step = "You are fully prepared to advance to the next lesson on your curriculum pathway."
    elif passed:
        summary = (
            f"Well done! You passed the assessment on {concept_title} with {score} out of {total_questions} "
            f"correct ({percentage}%). Your foundation is strong enough to advance."
        )
        strengths = [f"Solid grasp of fundamental operations and balance rules in {concept_title}.", "Active problem solving on diagnostic items."]
        if misconceptions:
            focus_area = f"Review the question where {misconceptions[0].replace('_', ' ')} occurred to ensure complete accuracy."
        else:
            focus_area = "Double check arithmetic transformations before finalizing solutions."
        action_step = "Review the step-by-step solution for the question you missed, then continue to your next lesson."
    else:
        summary = (
            f"You completed the assessment for {concept_title} scoring {score} of {total_questions} ({percentage}%). "
            f"Making errors is an essential and valuable step toward deep mathematical understanding."
        )
        strengths = ["Active engagement with non-trivial algebraic and arithmetic problem solving.", f"Persistence through all {total_questions} diagnostic questions."]
        if misconceptions:
            primary_misconception = misconceptions[0].replace('_', ' ')
            focus_area = f"The primary cognitive pattern identified was '{primary_misconception}'. Focus on verifying both sides of equations."
        else:
            focus_area = "Strengthen prerequisite step consistency and sign rules across transformations."
        action_step = "Carefully review the detailed question explanations below and practice the recommended prerequisite activity."

    return {
        "summary": summary,
        "strengths": strengths,
        "focus_area": focus_area,
        "action_step": action_step,
        "provider": "NCERT Curriculum Engine",
        "model": "curriculum_fallback",
        "is_fallback": True,
        "fallback_reason": fallback_reason or "Curriculum Grounded Engine"
    }


async def generate_assessment_guidance(
    concept_id: str,
    score: int,
    total_questions: int,
    percentage: float,
    passed: bool,
    outcome: str,
    missed_questions: List[Dict[str, Any]],
    misconceptions: List[str]
) -> Dict[str, Any]:
    """
    Asynchronously generates personalized learning guidance for a completed assessment.
    Attempts Google Gemini API first when active, gracefully falling back to deterministic NCERT guidance.
    """
    settings = get_ai_settings()
    concept = get_concept(concept_id.upper())
    concept_title = concept.title if concept else concept_id

    # If offline, testing, or unconfigured, use deterministic fallback
    is_offline = (
        settings.ai_offline_mode
        or not settings.ai_enable_gemini
        or not settings.gemini_api_key
        or "PYTEST_CURRENT_TEST" in os.environ
    )

    if is_offline:
        return _generate_fallback_guidance(
            concept_title=concept_title,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            passed=passed,
            outcome=outcome,
            missed_questions=missed_questions,
            misconceptions=misconceptions,
            fallback_reason="Offline or testing mode"
        )

    adapter = GeminiAdapter(settings)
    if not adapter.is_configured():
        return _generate_fallback_guidance(
            concept_title=concept_title,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            passed=passed,
            outcome=outcome,
            missed_questions=missed_questions,
            misconceptions=misconceptions,
            fallback_reason="Gemini adapter not configured"
        )

    # Build prompt for Gemini
    missed_summary = []
    for mq in missed_questions[:3]:
        q_prompt = mq.get("prompt", "")
        sel = mq.get("selected_option_text", mq.get("selected_option_id", ""))
        corr = mq.get("correct_option_text", mq.get("correct_option_id", ""))
        misc = mq.get("misconception_tag", "none")
        missed_summary.append(f"- Question: {q_prompt}\n  Student Answer: {sel}\n  Correct: {corr}\n  Pattern: {misc}")

    system_instruction = (
        f"You are SUTRA AI, an expert mathematics tutor specializing in NCERT Class 8 Mathematics.\n"
        f"The student completed an assessment on '{concept_title}'.\n"
        f"Score: {score}/{total_questions} ({percentage}%). Passed: {passed}. Adaptive outcome: {outcome}.\n"
        f"Diagnosed Misconceptions: {', '.join(misconceptions) if misconceptions else 'None'}.\n"
        f"Your task: Return a JSON object with EXACTLY four fields:\n"
        f"1. 'summary': A warm, encouraging pedagogical summary of their performance (2-3 sentences).\n"
        f"2. 'strengths': What the student did well or demonstrated understanding of.\n"
        f"3. 'focus_area': The exact mathematical principle or misconception to focus on.\n"
        f"4. 'action_step': Concrete, actionable next step for the student.\n"
        f"Respond ONLY with valid JSON. Do not include markdown codeblocks or preamble."
    )

    user_prompt = (
        f"Assessment Context:\n"
        f"Concept: {concept_title}\n"
        f"Score: {score}/{total_questions} ({percentage}%)\n"
        f"Passed: {passed}\n"
        f"Outcome: {outcome}\n"
        f"Misconceptions: {misconceptions}\n"
        f"Missed Questions Details:\n" + ("\n".join(missed_summary) if missed_summary else "All questions answered correctly.")
    )

    t0 = time.time()
    try:
        from google.genai import types
        config = types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=600,
            system_instruction=system_instruction
        )

        response = await adapter._client.aio.models.generate_content(
            model=adapter.model_id,
            contents=user_prompt,
            config=config
        )

        duration_ms = round((time.time() - t0) * 1000, 2)
        raw_text = response.text.strip() if response and response.text else ""

        # Parse JSON
        parsed = None
        # Clean potential markdown fences
        clean_json_str = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw_text, flags=re.MULTILINE).strip()
        try:
            parsed = json.loads(clean_json_str)
        except Exception:
            # Fallback regex extraction
            match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if match:
                try:
                    parsed = json.loads(match.group(0))
                except Exception:
                    pass

        if parsed and isinstance(parsed, dict) and "summary" in parsed:
            logger.info(f"Gemini generated assessment guidance in {duration_ms}ms")
            raw_strengths = parsed.get("strengths", [])
            if isinstance(raw_strengths, str):
                strengths_list = [raw_strengths] if raw_strengths else []
            elif isinstance(raw_strengths, list):
                strengths_list = [str(s) for s in raw_strengths]
            else:
                strengths_list = []

            return {
                "summary": parsed.get("summary", ""),
                "strengths": strengths_list,
                "focus_area": parsed.get("focus_area", ""),
                "action_step": parsed.get("action_step", ""),
                "provider": "Google Gemini",
                "model": adapter.model_id,
                "is_fallback": False,
                "latency_ms": duration_ms
            }
        else:
            logger.warning(f"Gemini returned non-JSON guidance: {raw_text[:100]}... Using fallback.")
            return _generate_fallback_guidance(
                concept_title=concept_title,
                score=score,
                total_questions=total_questions,
                percentage=percentage,
                passed=passed,
                outcome=outcome,
                missed_questions=missed_questions,
                misconceptions=misconceptions,
                fallback_reason="Non-JSON response from Gemini"
            )

    except Exception as e:
        logger.warning(f"Gemini guidance generation failed ({e}). Using deterministic curriculum fallback.")
        return _generate_fallback_guidance(
            concept_title=concept_title,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            passed=passed,
            outcome=outcome,
            missed_questions=missed_questions,
            misconceptions=misconceptions,
            fallback_reason=str(e)
        )
