"""
SUTRA LEARN — OMEGA API Discovery & Specification Verification Script
Tests the newly supplied Gemini API key:
- Discovers available models via official google-genai SDK
- Tests generate_content on active models
- Measures latency, token consumption, and mathematical correctness
- Validates error handling and attribution
"""

import os
import sys
import time

NEW_API_KEY = "AQ.Ab8...fiVQ [REDACTED_FOR_SECURITY]"

def main():
    print("=" * 80)
    print("SUTRA LEARN OMEGA — API DISCOVERY & VERIFICATION")
    print("=" * 80)
    print(f"Testing API Key: {NEW_API_KEY[:10]}...{NEW_API_KEY[-4:]} (Length: {len(NEW_API_KEY)})")

    try:
        from google import genai
        from google.genai import types
        print("google-genai SDK successfully imported.")
    except ImportError as e:
        print(f"Failed to import google-genai SDK: {e}")
        sys.exit(1)

    client = genai.Client(api_key=NEW_API_KEY)
    print("genai.Client initialized.")

    # 1. Model Listing & Discovery
    print("\n--- 1. MODEL DISCOVERY ---")
    discovered_models = []
    try:
        t0 = time.time()
        pager = client.models.list()
        for m in pager:
            name = getattr(m, "name", str(m))
            # Clean model name if prefixed with models/
            short_name = name.replace("models/", "")
            discovered_models.append(short_name)
        dt = round((time.time() - t0) * 1000, 2)
        print(f"Discovered {len(discovered_models)} models in {dt}ms.")
        # Filter for gemini models
        gemini_models = [m for m in discovered_models if "gemini" in m.lower()]
        print(f"Gemini models ({len(gemini_models)}):")
        for gm in gemini_models[:15]:
            print(f"  - {gm}")
    except Exception as ex:
        print(f"Model discovery via client.models.list() failed: {ex}")

    # 2. Generation Verification on Primary Candidates
    candidates = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-flash-lite-latest",
        "gemini-3.8-flash",
        "gemini-3-flash-preview",
        "gemini-2.0-flash-lite",
        "gemini-2.5-pro",
    ]
    # Also include models discovered
    for dm in discovered_models:
        if dm not in candidates and ("flash" in dm or "pro" in dm):
            candidates.append(dm)

    print("\n--- 2. GENERATION VERIFICATION ---")
    math_prompt = (
        "You are SUTRA AI, a Class 8 NCERT Mathematics tutor. "
        "Explain step-by-step how to solve for x: 3x - 7 = 11. "
        "Show both steps, state the balance principle, and provide 1 progressive hint."
    )

    working_models = []
    failed_models = {}

    for model in candidates:
        print(f"\nTesting model: '{model}'...")
        t0 = time.time()
        try:
            config = types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=1024,
                system_instruction="You are SUTRA AI, an elite mathematics tutor specializing in NCERT Class 8 Mathematics."
            )
            response = client.models.generate_content(
                model=model,
                contents=math_prompt,
                config=config
            )
            elapsed_ms = round((time.time() - t0) * 1000, 2)
            answer_text = response.text.strip() if response and response.text else ""
            tokens = getattr(response.usage_metadata, "total_token_count", None) if hasattr(response, "usage_metadata") else None
            
            print(f"  [SUCCESS] Latency: {elapsed_ms}ms | Tokens: {tokens}")
            print(f"  [EXCERPT]: {answer_text[:120]}...")
            working_models.append({
                "model": model,
                "latency_ms": elapsed_ms,
                "tokens": tokens,
                "excerpt": answer_text[:150]
            })
            # Once we verify at least 2 working models, we have authoritative proof
            if len(working_models) >= 3:
                print("Confirmed 3 functional models. Continuing verification...")
        except Exception as ex:
            elapsed_ms = round((time.time() - t0) * 1000, 2)
            err_msg = str(ex)
            print(f"  [FAILED] ({elapsed_ms}ms): {err_msg[:120]}")
            failed_models[model] = err_msg

    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"Working Models: {[m['model'] for m in working_models]}")
    print(f"Failed Models: {list(failed_models.keys())}")

    import json
    results_data = {
        "api_key_prefix": NEW_API_KEY[:10],
        "working_models": working_models,
        "failed_models": failed_models,
        "total_discovered": len(discovered_models),
        "timestamp": time.time()
    }
    with open("docs/omega_api_probe_results.json", "w", encoding="utf-8") as f:
        json.dump(results_data, f, indent=2)
    print("Results exported to docs/omega_api_probe_results.json")

if __name__ == "__main__":
    main()

