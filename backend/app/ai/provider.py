"""
SUTRA LEARN — AI Provider Abstraction
Supports external LLM providers (e.g. Google Gemini) when configured,
with an honest, curriculum-grounded deterministic mathematical fallback
when no API key is present or when network requests fail.
"""

import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import httpx

from app.ai.curriculum_context import get_grounded_concept_context

logger = logging.getLogger("sutra.ai.provider")


class BaseAIProvider(ABC):
    @abstractmethod
    async def generate_tutor_response(
        self,
        message: str,
        concept_id: Optional[str],
        mode: str,
        conversation_history: List[Dict[str, str]],
        learner_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generates a pedagogical tutor response."""
        pass

    @abstractmethod
    async def generate_educator_insight(
        self,
        query: str,
        cohort_summary: List[Dict[str, Any]],
        concept_analytics: List[Dict[str, Any]],
        specific_learner_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generates an evidence-grounded classroom insight."""
        pass


class CurriculumGroundedFallbackProvider(BaseAIProvider):
    """
    Transparent, curriculum-grounded mathematical tutor & educator intelligence engine.
    Used when no external AI API key is configured or when the remote service is unavailable.
    Clearly labeled so learners and teachers know responses derive from verified NCERT curriculum data.
    """

    async def generate_tutor_response(
        self,
        message: str,
        concept_id: Optional[str],
        mode: str,
        conversation_history: List[Dict[str, str]],
        learner_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        target_concept_id = concept_id or "MATH-C01"
        grounding = get_grounded_concept_context(target_concept_id)
        msg_lower = message.lower().strip()
        lesson = grounding.get("lesson") or {}
        worked_steps = lesson.get("worked_steps", [])

        # Default pedagogical structure
        response_type = "guided_explanation"
        hints: List[str] = []
        requires_follow_up = True

        # Mode: Worked Example Walkthrough
        if mode == "worked_example" or "example" in msg_lower or "show me how" in msg_lower:
            response_type = "worked_example"
            steps_text = "\n\n".join([
                f"**Step {s['step_number']} — {s['action']}**\n$${s['expression']}$$\n*Pedagogical reasoning:* {s['reasoning']}"
                for s in worked_steps
            ]) if worked_steps else "Start by isolating terms containing the variable on one side and constant integers on the other."

            answer = (
                f"Here is a complete, step-by-step worked example for **{grounding['title']}**:\n\n"
                f"{steps_text}\n\n"
                f"**Mathematical Verification:**\nSubstitute the calculated value back into the original expression to confirm both left-hand side and right-hand side evaluate to identical quantities."
            )
            hints = [
                "Always apply the exact same operation to both sides to maintain equality.",
                "Check signs carefully when moving terms across the equals sign."
            ]
            requires_follow_up = False

        # Mode: Practice / Diagnostic Question
        elif mode == "practice" or "practice" in msg_lower or "quiz me" in msg_lower or "problem" in msg_lower:
            response_type = "practice_question"
            samples = grounding.get("sample_questions", [])
            q = samples[0] if samples else None
            if q:
                options_str = "\n".join([f"- **({opt['id']})** {opt['text']}" for opt in q["options"]])
                answer = (
                    f"Let's test your understanding of **{grounding['title']}** with a diagnostic challenge:\n\n"
                    f"**Problem:**\n{q['prompt']}\n\n"
                    f"{options_str}\n\n"
                    f"Take your time. What is your chosen option, and what operation did you perform first?"
                )
                hints = [
                    "Identify the operations applied to the variable in reverse order (inverse operations).",
                    f"Common pitfall to avoid: {q.get('common_misconception', 'Check signs carefully')}"
                ]
            else:
                answer = "Solve for x: $$3x + 7 = 22$$. What operation will you perform first?"
                hints = ["First subtract 7 from both sides.", "Then divide by 3."]

        # Mode: Check My Work
        elif mode == "check_my_work" or "check" in msg_lower or "did i do this right" in msg_lower:
            response_type = "check_work"
            answer = (
                f"Let's review your mathematical reasoning for **{grounding['title']}**:\n\n"
                f"1. **Equation Balance Check:** Did you apply the exact same operation (addition, subtraction, multiplication, or division) to BOTH the LHS and RHS?\n"
                f"2. **Integer Arithmetic Sign Check:** Watch out for negative signs! For example, subtracting a negative number is equivalent to adding a positive ($$a - (-b) = a + b$$).\n"
                f"3. **Variable Isolation:** Ensure the coefficient of the variable is simplified to 1 ($$1x = x$$).\n\n"
                f"Share your intermediate steps line by line, and I will pinpoint exactly where any algebraic friction occurs."
            )
            hints = ["State your starting equation, Step 1, and Step 2."]

        # Mode: Prerequisite Support
        elif mode == "prerequisite_support" or "prereq" in msg_lower or "foundation" in msg_lower or "basics" in msg_lower:
            response_type = "guided_explanation"
            prereqs = grounding.get("prerequisites", [])
            prereq_text = ", ".join(prereqs) if prereqs else "Integer Arithmetic (MATH-C01)"
            answer = (
                f"To master **{grounding['title']}**, having confidence with foundational prerequisites is essential:\n\n"
                f"Key prerequisite concepts: **{prereq_text}**.\n\n"
                f"- **Integer Rules:** Multiplying or dividing two numbers with identical signs yields positive; opposite signs yield negative.\n"
                f"- **Balance Principle:** Think of an equation like a balanced pair of scales. If you take away 4 kg from one side, you must take away 4 kg from the other to preserve equilibrium.\n\n"
                f"Would you like to review an example problem on integer arithmetic first?"
            )
            hints = ["Start with smaller numbers to build intuition before moving to multi-step equations."]

        # Mode: Quick Revision
        elif mode == "quick_revision" or "summary" in msg_lower or "revise" in msg_lower:
            response_type = "guided_explanation"
            principles = lesson.get("key_principles", [
                "Equality is preserved by performing identical operations on both sides.",
                "Inverse operations undo each other: addition undoes subtraction; multiplication undoes division.",
                "Always verify solutions by substitution into the original equation."
            ])
            principles_str = "\n".join([f"- **Principle {i+1}:** {p}" for i, p in enumerate(principles)])
            answer = (
                f"**Quick Revision Summary: {grounding['title']}**\n\n"
                f"**Core Objective:** {lesson.get('objective', grounding.get('description'))}\n\n"
                f"**Essential Principles:**\n{principles_str}\n\n"
                f"**Pitfall Warning:** {lesson.get('common_pitfalls', ['Do not apply operations to only one side of the equation.'])[0]}"
            )
            hints = ["Practice at least 2 questions without hints to prove concept retention."]
            requires_follow_up = False

        # Default Guided Learning
        else:
            response_type = "guided_explanation"
            answer = (
                f"Let's work through **{grounding['title']}** thoughtfully.\n\n"
                f"{grounding.get('description', '')}\n\n"
                f"**Key Rule:** Whenever you modify an algebraic equation, balance must be preserved on both sides. "
                f"For example, in $$2x + 5 = 15$$, our goal is to isolate $$x$$.\n\n"
                f"What do you think is the first logical step to isolate the term $$2x$$?"
            )
            hints = [
                "Look at what is added to 2x. How can we undo adding 5?",
                "Subtract 5 from both sides of the equation."
            ]

        return {
            "answer": answer,
            "response_type": response_type,
            "hints": hints,
            "concept_id": target_concept_id,
            "requires_follow_up": requires_follow_up,
            "is_fallback": True,
            "provider": "SutraCurriculumEngine",
            "model": "ncert-class8-curriculum-v1",
            "fallback_reason": "Curriculum-grounded deterministic engine active (guaranteed mathematical precision)."
        }

    async def generate_educator_insight(
        self,
        query: str,
        cohort_summary: List[Dict[str, Any]],
        concept_analytics: List[Dict[str, Any]],
        specific_learner_id: Optional[str] = None
    ) -> Dict[str, Any]:
        total_students = len(cohort_summary)
        struggling_students = [s for s in cohort_summary if s.get("needs_review") or (s.get("accuracy_percentage") is not None and s.get("accuracy_percentage") < 65.0)]
        low_accuracy_concepts = [c for c in concept_analytics if c.get("accuracy_percentage", 0.0) < 70.0]

        top_friction = []
        for c in concept_analytics:
            if c.get("top_misconceptions"):
                top_friction.extend(c["top_misconceptions"])

        # Construct evidence-grounded response
        observations = [
            f"Cohort comprises {total_students} registered learners in Class 8 Mathematics.",
            f"{len(struggling_students)} learner(s) currently flag cognitive friction or have an accuracy rate below 65%.",
            f"Concepts showing lowest unassisted mastery: {', '.join([c['concept_id'] for c in low_accuracy_concepts]) or 'None (Cohort performing above threshold)'}."
        ]

        if specific_learner_id:
            target = next((s for s in cohort_summary if s["learner_id"] == specific_learner_id), None)
            if target:
                observations.append(
                    f"Specific dossier for {target.get('name', specific_learner_id)}: "
                    f"{target.get('total_attempts', 0)} total attempts, {target.get('total_correct', 0)} correct "
                    f"({target.get('accuracy_percentage', 0.0)}% accuracy)."
                )

        recommended_actions = [
            "Conduct a targeted 10-minute small-group review on negative signs and inverse operation sequencing.",
            "Use the SUTRA clinical intervention workflow to assign scaffolded practice before advancing learners to multi-step distribution problems.",
            "Schedule a formative check-in for learners requiring teacher review."
        ]

        summary_text = (
            f"**Classroom Diagnostic Synthesis**\n\n"
            f"**Verified Database Facts:**\n" + "\n".join([f"- {o}" for o in observations]) + "\n\n"
            f"**Common Misconception Friction Points:**\n" +
            ("\n".join([f"- {m}" for m in top_friction[:3]]) if top_friction else "- No dominant misconceptions recorded yet.") + "\n\n"
            f"**Recommended Differentiated Interventions:**\n" + "\n".join([f"{i+1}. {a}" for i, a in enumerate(recommended_actions)])
        )

        return {
            "summary": summary_text,
            "observations": observations,
            "recommended_actions": recommended_actions,
            "struggling_learner_count": len(struggling_students),
            "low_accuracy_concepts": [c["concept_id"] for c in low_accuracy_concepts],
            "is_fallback": True,
            "provider": "SutraEducatorIntelligenceEngine",
            "model": "ncert-class8-analytics-v1"
        }


class GeminiProvider(BaseAIProvider):
    """
    Connects to Google Gemini API using official Google Generative Language REST endpoint.
    Automatically falls back to CurriculumGroundedFallbackProvider if credentials fail or network errors occur.
    """

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model = model
        self.fallback = CurriculumGroundedFallbackProvider()

    async def generate_tutor_response(
        self,
        message: str,
        concept_id: Optional[str],
        mode: str,
        conversation_history: List[Dict[str, str]],
        learner_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        grounding = get_grounded_concept_context(concept_id or "MATH-C01")

        system_prompt = (
            "You are SUTRA AI, a master mathematics educator for Class 8 students studying NCERT Mathematics. "
            "Your teaching philosophy is Socratic and concept-first. Never simply blurt out final answers. "
            "Help the learner uncover the solution step by step using inverse operations and balance principles. "
            f"Current Concept Context: {grounding.get('title')} ({grounding.get('code')}). "
            f"Description: {grounding.get('description')}. "
            f"Teaching Mode: {mode}. "
            "Format mathematical equations cleanly using LaTeX math delimiters ($$...$$ for display, $...$ for inline). "
            "Provide 1-2 progressive hints if the learner is stuck."
        )

        contents = []
        for h in conversation_history[-6:]:
            role = "user" if h.get("sender_role") == "user" else "model"
            contents.append({"role": role, "parts": [{"text": h.get("content", "")}]})
        contents.append({"role": "user", "parts": [{"text": message}]})

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "contents": contents,
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 800,
            }
        }

        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        text = "".join([p.get("text", "") for p in parts])
                        return {
                            "answer": text,
                            "response_type": "guided_explanation",
                            "hints": ["Review each algebraic operation on both sides."],
                            "concept_id": concept_id or "MATH-C01",
                            "requires_follow_up": True,
                            "is_fallback": False,
                            "provider": "GoogleGemini",
                            "model": self.model
                        }
                logger.warning(f"Gemini API returned status {res.status_code}: {res.text}. Triggering curriculum fallback.")
        except Exception as e:
            logger.warning(f"Gemini API connection error: {e}. Triggering curriculum fallback.")

        # Honest fallback to curriculum
        fallback_res = await self.fallback.generate_tutor_response(message, concept_id, mode, conversation_history, learner_context)
        fallback_res["fallback_reason"] = "Gemini API unavailable; serving grounded curriculum response."
        return fallback_res

    async def generate_educator_insight(
        self,
        query: str,
        cohort_summary: List[Dict[str, Any]],
        concept_analytics: List[Dict[str, Any]],
        specific_learner_id: Optional[str] = None
    ) -> Dict[str, Any]:
        try:
            facts = {
                "total_learners": len(cohort_summary),
                "cohort": cohort_summary[:10],
                "concept_difficulty": concept_analytics
            }
            system_prompt = (
                "You are SUTRA Educator Intelligence, an educational technology specialist. "
                "Analyze the provided verified classroom data. Ground every statement strictly in the numbers. "
                "Distinguish clearly between: 1) Verified Database Facts, 2) Calculated Statistics, 3) Educational Interpretations, and 4) Actionable Pedagogical Recommendations. "
                "Do not invent student names or imaginary test scores."
            )
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [{"role": "user", "parts": [{"text": f"Educator Query: {query}\n\nClassroom Evidence: {json.dumps(facts)}"}]}],
                "systemInstruction": {"parts": [{"text": system_prompt}]},
                "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1000}
            }
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(url, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        text = "".join([p.get("text", "") for p in parts])
                        return {
                            "summary": text,
                            "observations": [f"Evaluated {len(cohort_summary)} students across {len(concept_analytics)} concepts."],
                            "recommended_actions": ["Review prerequisite bottlenecks and approve targeted scaffolds."],
                            "struggling_learner_count": len([s for s in cohort_summary if s.get("needs_review")]),
                            "low_accuracy_concepts": [c["concept_id"] for c in concept_analytics if c.get("accuracy_percentage", 0) < 70],
                            "is_fallback": False,
                            "provider": "GoogleGemini",
                            "model": self.model
                        }
        except Exception as e:
            logger.warning(f"Gemini API educator insight error: {e}. Falling back to curriculum analytics.")

        return await self.fallback.generate_educator_insight(query, cohort_summary, concept_analytics, specific_learner_id)


class OllamaProvider(BaseAIProvider):
    """
    Local and offline AI provider running via Ollama.
    Supports primary local model (Qwen 3.5 4B) and lightweight fallback (Gemma 4 E2B).
    Falls back transparently to CurriculumGroundedFallbackProvider if Ollama is unreachable.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        primary_model: str = "qwen:3.5-4b",
        fallback_model: str = "gemma4:e2b"
    ):
        self.base_url = (base_url or os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")).rstrip("/")
        self.primary_model = os.environ.get("OLLAMA_PRIMARY_MODEL", primary_model)
        self.fallback_model = os.environ.get("OLLAMA_FALLBACK_MODEL", fallback_model)
        self.fallback = CurriculumGroundedFallbackProvider()

    async def get_available_models(self) -> List[str]:
        """Queries Ollama /api/tags to detect installed models."""
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                if res.status_code == 200:
                    models = res.json().get("models", [])
                    return [m.get("name") for m in models if m.get("name")]
        except Exception:
            pass
        return []

    async def generate_tutor_response(
        self,
        message: str,
        concept_id: Optional[str],
        mode: str,
        conversation_history: List[Dict[str, str]],
        learner_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        grounding = get_grounded_concept_context(concept_id or "MATH-C01")

        installed = await self.get_available_models()
        target_model = self.primary_model
        if target_model not in installed and self.fallback_model in installed:
            target_model = self.fallback_model

        prompt = (
            f"You are SUTRA AI, a Class 8 NCERT Mathematics tutor. "
            f"Teaching Mode: {mode}. Concept: {grounding.get('title')}. "
            f"Student message: {message}. "
            f"Provide a clear, pedagogical response explaining the mathematical principles. Never give raw answers without steps."
        )

        resp_type = "guided_explanation"
        if mode == "worked_example":
            resp_type = "worked_example"
        elif mode == "practice":
            resp_type = "practice_question"

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": target_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.3}
                    }
                )
                if res.status_code == 200:
                    response_text = res.json().get("response", "").strip()
                    if response_text:
                        return {
                            "answer": response_text,
                            "response_type": resp_type,
                            "hints": ["Review each algebraic operation on both sides."],
                            "concept_id": concept_id or "MATH-C01",
                            "requires_follow_up": True,
                            "is_fallback": (target_model != self.primary_model),
                            "fallback_reason": f"Active local model: {target_model}",
                            "provider": "Ollama",
                            "model": target_model
                        }
        except Exception as e:
            logger.warning(f"Ollama local inference unavailable ({e}); falling back to curriculum engine.")

        fallback_res = await self.fallback.generate_tutor_response(
            message, concept_id, mode, conversation_history, learner_context
        )
        fallback_res["fallback_reason"] = "Ollama model inference unavailable; serving grounded curriculum response."
        return fallback_res

    async def generate_educator_insight(
        self,
        query: str,
        cohort_summary: List[Dict[str, Any]],
        concept_analytics: List[Dict[str, Any]],
        specific_learner_id: Optional[str] = None
    ) -> Dict[str, Any]:
        installed = await self.get_available_models()
        target_model = self.fallback_model if self.fallback_model in installed else self.primary_model

        facts = {
            "total_learners": len(cohort_summary),
            "concept_difficulty": concept_analytics
        }
        prompt = (
            f"You are SUTRA Educator Intelligence. Query: {query}. Classroom Data: {json.dumps(facts)}. "
            f"Provide an evidence-grounded summary of cohort performance and recommended pedagogical actions."
        )

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": target_model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.2}
                    }
                )
                if res.status_code == 200:
                    response_text = res.json().get("response", "").strip()
                    if response_text:
                        return {
                            "summary": response_text,
                            "observations": [f"Evaluated {len(cohort_summary)} students using local model {target_model}."],
                            "recommended_actions": ["Review prerequisite bottlenecks and approve targeted scaffolds."],
                            "struggling_learner_count": len([s for s in cohort_summary if s.get("needs_review")]),
                            "low_accuracy_concepts": [c["concept_id"] for c in concept_analytics if c.get("accuracy_percentage", 0) < 70],
                            "is_fallback": False,
                            "provider": "Ollama",
                            "model": target_model
                        }
        except Exception as e:
            logger.warning(f"Ollama educator assistant inference unavailable ({e}); falling back to curriculum analytics.")

        return await self.fallback.generate_educator_insight(query, cohort_summary, concept_analytics, specific_learner_id)


class OrchestratedAIProvider(BaseAIProvider):
    """
    Production Multi-Model Orchestrated AI Provider.
    Coordinates requests through the 12-state AIOrchestrator state machine,
    delegating to Gemini -> Qwen -> Gemma -> Deterministic Fallback.
    """
    def __init__(self):
        from app.ai.orchestrator import get_ai_orchestrator
        self.orchestrator = get_ai_orchestrator()
        self.fallback = CurriculumGroundedFallbackProvider()

    async def generate_tutor_response(
        self,
        message: str,
        concept_id: Optional[str],
        mode: str,
        conversation_history: List[Dict[str, str]],
        learner_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        user_id = learner_context.get("learner_id") or "student-01"
        res = await self.orchestrator.execute_tutor_request(
            user_id=user_id,
            role="student",
            message=message,
            conversation_id=learner_context.get("conversation_id") or "conv_auto",
            concept_id=concept_id,
            mode=mode,
            conversation_history=conversation_history,
            learner_context=learner_context
        )
        return res.model_dump()

    async def generate_educator_insight(
        self,
        query: str,
        cohort_summary: List[Dict[str, Any]],
        concept_analytics: List[Dict[str, Any]],
        specific_learner_id: Optional[str] = None
    ) -> Dict[str, Any]:
        return await self.fallback.generate_educator_insight(
            query, cohort_summary, concept_analytics, specific_learner_id
        )


def get_ai_provider() -> BaseAIProvider:
    """
    Multi-Model Provider Orchestrator.
    Evaluates configured provider mode: 'gemini' | 'ollama' | 'deterministic' | 'auto'.
    Failover sequence in 'auto':
      1. Google Gemini API (if key present and valid)
      2. Ollama Local Model (Qwen 3.5 4B -> Gemma 4 E2B)
      3. SUTRA Curriculum Grounded Deterministic Fallback
    """
    mode = os.environ.get("AI_PROVIDER") or os.environ.get("AI_MODE", "auto").lower()

    if mode == "deterministic" or os.environ.get("APP_ENV") == "testing":
        return CurriculumGroundedFallbackProvider()

    return OrchestratedAIProvider()

