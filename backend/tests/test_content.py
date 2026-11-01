"""
Unit tests for curriculum content integrity, prerequisite graph acyclicity,
and comprehensive mathematical question-bank validation.
"""

from app.content.concepts import CONCEPTS_REGISTRY, get_prerequisite_graph
from app.content.questions import QUESTIONS_REGISTRY, get_all_questions, get_questions_by_concept
from app.content.models import MisconceptionTag


def test_prerequisite_graph_acyclic():
    """Ensure the concept dependency graph is a valid Directed Acyclic Graph (DAG)."""
    graph = get_prerequisite_graph()
    visited = set()
    visiting = set()

    def dfs(node: str):
        visiting.add(node)
        for neighbor in graph.get(node, []):
            assert neighbor in graph, f"Prerequisite {neighbor} of {node} does not exist in registry!"
            assert neighbor not in visiting, f"Cycle detected in prerequisite graph involving {node} -> {neighbor}!"
            if neighbor not in visited:
                dfs(neighbor)
        visiting.remove(node)
        visited.add(node)

    for concept_id in graph:
        if concept_id not in visited:
            dfs(concept_id)


def test_all_concepts_have_lessons():
    """Verify all concepts contain complete pedagogical lesson structures."""
    assert len(CONCEPTS_REGISTRY) >= 6
    for c_id, concept in CONCEPTS_REGISTRY.items():
        assert concept.lesson is not None
        assert len(concept.lesson.key_principles) >= 2
        assert len(concept.lesson.worked_steps) >= 2
        assert len(concept.lesson.common_pitfalls) >= 1
        assert len(concept.lesson.interactive_prompt) > 0


def test_question_bank_depth_and_rigor():
    """Verify core baseline concepts have >= 5 questions and all concepts have >= 2 questions."""
    all_q = get_all_questions()
    assert len(all_q) >= 30, f"Expected at least 30 questions in bank, found {len(all_q)}"

    for c_id in ["MATH-C01", "MATH-C02", "MATH-C03", "MATH-C04", "MATH-C05", "MATH-C06"]:
        concept_questions = get_questions_by_concept(c_id)
        assert len(concept_questions) >= 5, (
            f"Baseline Concept {c_id} has only {len(concept_questions)} questions; minimum 5 required."
        )

    for c_id in CONCEPTS_REGISTRY:
        concept_questions = get_questions_by_concept(c_id)
        assert len(concept_questions) >= 2, (
            f"Concept {c_id} has only {len(concept_questions)} questions; minimum 2 required."
        )


def test_question_integrity_and_options():
    """Verify every question has valid concept pointers, 4 unique options, and exactly 1 correct answer."""
    questions = get_all_questions()
    seen_q_ids = set()

    for q in questions:
        # Unique question ID
        assert q.id not in seen_q_ids, f"Duplicate question ID: {q.id}"
        seen_q_ids.add(q.id)

        # Must reference valid concept
        assert q.concept_id in CONCEPTS_REGISTRY, f"Question {q.id} references invalid concept {q.concept_id}"

        # Prerequisites must exist
        for pr in q.prerequisite_ids:
            assert pr in CONCEPTS_REGISTRY, f"Question {q.id} references invalid prerequisite {pr}"

        # Option validation: exactly 4 options
        assert len(q.options) == 4, f"Question {q.id} must have exactly 4 options, found {len(q.options)}"
        correct_count = 0
        option_ids = set()
        option_texts = set()

        for opt in q.options:
            assert opt.id in ["A", "B", "C", "D"], f"Invalid option ID {opt.id} in {q.id}"
            assert opt.id not in option_ids, f"Duplicate option ID {opt.id} in {q.id}"
            option_ids.add(opt.id)

            assert opt.text not in option_texts, f"Duplicate option text in {q.id}: '{opt.text}'"
            option_texts.add(opt.text)

            if opt.is_correct:
                correct_count += 1
                assert opt.id == q.correct_option_id, f"Question {q.id} correct_option_id mismatch"
            else:
                if opt.misconception_tag != MisconceptionTag.NONE:
                    assert opt.misconception_explanation is not None, (
                        f"Question {q.id} option {opt.id} has misconception tag but no explanation."
                    )

        assert correct_count == 1, f"Question {q.id} must have exactly one correct option, found {correct_count}"
        assert len(q.hint) >= 10, f"Question {q.id} hint too short"
        assert len(q.explanation) >= 15, f"Question {q.id} explanation too short"
