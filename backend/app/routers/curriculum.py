"""
SUTRA LEARN - Curriculum & Concepts API Router
Provides concept graph, detailed lessons, and prerequisite gating logic.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Header
from app.content.concepts import get_all_concepts, get_concept, get_prerequisite_graph
from app.content.questions import get_questions_by_concept
from app.db.database import get_db_connection
from app.db import crud
from app.schemas import ConceptSummary, ConceptDetail, AssessmentQuestionOut

router = APIRouter(prefix="/api/v1", tags=["Curriculum"])


@router.get("/concepts", response_model=Dict[str, Any])
def list_concepts(
    x_user_id: Optional[str] = Header(None, alias="x-user-id"),
    conn=Depends(get_db_connection)
):
    concepts = get_all_concepts()
    graph = get_prerequisite_graph()

    # If user identity provided, calculate prerequisite lock status
    user_progress_map = {}
    if x_user_id:
        p_rows = crud.get_learner_progress(conn, x_user_id)
        for r in p_rows:
            user_progress_map[r["concept_id"]] = r["status"]

    annotated_concepts = []
    for c in concepts:
        c_dict = c.model_dump()
        missing_prereqs = []
        is_unlocked = True

        if c.prerequisites:
            for p_id in c.prerequisites:
                p_status = user_progress_map.get(p_id, "not_started")
                # Prerequisite is satisfied if in_progress or mastered
                if p_status not in ["in_progress", "mastered"]:
                    is_unlocked = False
                    missing_prereqs.append(p_id)

        c_dict["is_unlocked"] = is_unlocked
        c_dict["missing_prerequisites"] = missing_prereqs
        annotated_concepts.append(c_dict)

    return {
        "curriculum": "Class 8 Mathematics - Linear Equations",
        "concepts": annotated_concepts,
        "prerequisite_graph": graph
    }


@router.get("/concepts/{concept_id}", response_model=ConceptDetail)
def read_concept(concept_id: str):
    try:
        concept = get_concept(concept_id.upper())
        return ConceptDetail(**concept.model_dump())
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Concept '{concept_id}' not found.")


@router.get("/concepts/{concept_id}/questions", response_model=List[AssessmentQuestionOut])
def list_concept_questions(concept_id: str):
    c_id = concept_id.upper()
    try:
        get_concept(c_id)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Concept '{concept_id}' not found.")

    questions = get_questions_by_concept(c_id)
    return [
        AssessmentQuestionOut(
            id=q.id,
            concept_id=q.concept_id,
            prompt=q.prompt,
            equation_display=q.equation_display,
            options=q.options,
            hint=q.hint,
            difficulty=q.difficulty,
            cognitive_demand=q.cognitive_demand
        )
        for q in questions
    ]
