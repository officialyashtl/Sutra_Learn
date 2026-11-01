import sys
import json
import asyncio
import time

sys.path.insert(0, "backend")
from app.ai.registry import get_ai_registry

async def main():
    reg = get_ai_registry()
    is_avail = await reg.qwen.is_available()
    if not is_avail:
        print(json.dumps({"status": "UNAVAILABLE", "message": "Model qwen3.5:4b is not available in Ollama"}))
        sys.exit(1)

    start = time.time()
    try:
        # Prompt asking for a concise mathematical response
        res = await reg.qwen.generate_tutor_response(
            message="State what the equals sign means in 10 words or less.",
            concept_id="MATH-C01",
            mode="explain_concept",
            conversation_history=[],
            learner_context={}
        )
        latency = round((time.time() - start) * 1000, 2)
        print(json.dumps({
            "status": "SUCCESS",
            "model": res.get("model"),
            "latency_ms": latency,
            "answer": res.get("answer"),
            "tokens_used": res.get("tokens_used")
        }))
    except Exception as e:
        print(json.dumps({"status": "ERROR", "error": str(e), "elapsed_ms": round((time.time() - start) * 1000, 2)}))
        sys.exit(1)

asyncio.run(main())

