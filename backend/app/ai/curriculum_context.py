"""
SUTRA LEARN — Curriculum Context Retrieval for SUTRA AI
Grounds AI responses directly in NCERT Class 8 Mathematics concepts,
learning objectives, worked steps, and diagnostic question structures.
"""

from typing import Dict, Any, Optional, List
import sqlite3
from app.content.concepts import CONCEPTS_REGISTRY
from app.content.questions import QUESTIONS_REGISTRY, get_questions_by_concept


def get_grounded_concept_context(concept_id: str) -> Dict[str, Any]:
    """Retrieves full curriculum grounding for a concept."""
    concept = CONCEPTS_REGISTRY.get(concept_id)
    if not concept:
        return {
            "concept_id": concept_id,
            "found": False,
            "title": "Mathematics General Topic",
            "description": "General linear equations and foundational mathematics."
        }

    lesson_data = None
    if concept.lesson:
        lesson_data = {
            "title": concept.lesson.title,
            "objective": concept.lesson.objective,
            "key_principles": concept.lesson.key_principles,
            "worked_steps": [s.model_dump() for s in concept.lesson.worked_steps],
            "common_pitfalls": concept.lesson.common_pitfalls,
            "interactive_prompt": concept.lesson.interactive_prompt,
        }

    questions = get_questions_by_concept(concept_id)
    question_summaries = [
        {
            "id": q.id,
            "prompt": q.prompt,
            "difficulty": q.difficulty,
            "correct_option_id": q.correct_option_id,
            "options": [{"id": opt.id, "text": opt.text, "misconception_explanation": opt.misconception_explanation} for opt in q.options],
            "hint": q.hint,
            "explanation": q.explanation,
            "common_misconception": "none",
        }
        for q in questions[:3]
    ]

    return {
        "concept_id": concept.id,
        "code": concept.code,
        "title": concept.title,
        "grade": concept.grade,
        "description": concept.description,
        "prerequisites": concept.prerequisites,
        "lesson": lesson_data,
        "sample_questions": question_summaries,
        "found": True,
    }


def get_learner_context(conn: sqlite3.Connection, learner_id: str, concept_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Safely retrieves the learner's own authorized performance signals.
    Never exposes other learners' private data.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, role FROM learners WHERE id = ?", (learner_id,))
    learner = cursor.fetchone()
    if not learner:
        return {"learner_id": learner_id, "found": False}

    # Fetch recent attempts
    query = """
        SELECT question_id, concept_id, is_correct, hint_used, misconception_tag, client_timestamp
        FROM attempts
        WHERE learner_id = ?
    """
    params = [learner_id]
    if concept_id:
        query += " AND concept_id = ?"
        params.append(concept_id)
    query += " ORDER BY server_timestamp DESC LIMIT 6"

    cursor.execute(query, tuple(params))
    recent_attempts = [dict(r) for r in cursor.fetchall()]

    # Check for active misconceptions
    misconceptions = [a["misconception_tag"] for a in recent_attempts if a["misconception_tag"] != "none"]

    return {
        "learner_id": learner["id"],
        "name": learner["name"],
        "grade": learner["grade"],
        "recent_attempts_count": len(recent_attempts),
        "recent_misconceptions": list(set(misconceptions)),
        "found": True,
    }
