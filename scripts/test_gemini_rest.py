"""
Comprehensive probe of the supplied Gemini API key:
- Tests REST endpoint and google-genai SDK
- Tests models list
- Tests generateContent on primary models (gemini-2.5-flash, gemini-flash-latest, etc.)
- Records latency, token counts, mathematical output
- Writes results to docs/omega_api_probe_results.json
"""
import urllib.request
import urllib.error
import json
import ssl
import time

API_KEY = "AQ.Ab8...fiVQ [REDACTED_FOR_SECURITY]"

def main():
    print("=" * 70)
    print("SUTRA LEARN OMEGA — API DISCOVERY AND REAL PROBE")
    print("=" * 70)

    # 1. Discover Models
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "SutraLearn-Omega/1.0"})
    
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        model_objs = data.get("models", [])
        models_list = [m.get("name", "").replace("models/", "") for m in model_objs]
        discovery_latency_ms = round((time.time() - t0) * 1000, 2)

    print(f"Discovered {len(models_list)} models in {discovery_latency_ms}ms.")
    
    # 2. Select candidates for generation testing
    candidates = [
        "gemini-2.5-flash",
        "gemini-flash-latest",
        "gemini-flash-lite-latest",
        "gemini-2.5-flash-lite",
        "gemini-2.5-pro",
        "gemini-pro-latest"
    ]
    # Filter to only those in discovered models
    valid_candidates = [c for c in candidates if c in models_list]
    print(f"Valid candidates to test: {valid_candidates}")

    # 3. Test generateContent for each candidate
    working_models = []
    failed_models = {}

    math_question = (
        "Solve for x step by step: 5x - 3 = 2x + 9. "
        "State the balance principle and provide 1 progressive hint."
    )

    for model_name in valid_candidates:
        post_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": math_question}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 1024
            },
            "systemInstruction": {
                "parts": [
                    {"text": "You are SUTRA AI, an elite mathematics tutor specializing in NCERT Class 8 Mathematics."}
                ]
            }
        }
        body_bytes = json.dumps(payload).encode("utf-8")
        post_req = urllib.request.Request(
            post_url,
            data=body_bytes,
            headers={
                "Content-Type": "application/json",
                "User-Agent": "SutraLearn-Omega/1.0"
            },
            method="POST"
        )
        t_req = time.time()
        try:
            with urllib.request.urlopen(post_req, timeout=15, context=ctx) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                latency_ms = round((time.time() - t_req) * 1000, 2)
                
                # Extract text
                candidates_out = resp_data.get("candidates", [])
                text_content = ""
                if candidates_out:
                    parts = candidates_out[0].get("content", {}).get("parts", [])
                    text_content = "".join([p.get("text", "") for p in parts])
                
                usage = resp_data.get("usageMetadata", {})
                tokens = usage.get("totalTokenCount")
                
                print(f"\n[PASS] Model '{model_name}' | Latency: {latency_ms}ms | Tokens: {tokens}")
                print(f"Excerpt: {text_content[:140]}...")
                
                working_models.append({
                    "model": model_name,
                    "latency_ms": latency_ms,
                    "tokens": tokens,
                    "excerpt": text_content[:200],
                    "status": "OPERATIONAL"
                })
        except urllib.error.HTTPError as e:
            latency_ms = round((time.time() - t_req) * 1000, 2)
            err_body = e.read().decode("utf-8", errors="replace")
            print(f"\n[FAIL] Model '{model_name}' HTTP {e.code} ({latency_ms}ms): {err_body[:160]}")
            failed_models[model_name] = f"HTTP {e.code}: {err_body[:200]}"
        except Exception as ex:
            latency_ms = round((time.time() - t_req) * 1000, 2)
            print(f"\n[FAIL] Model '{model_name}' Exception ({latency_ms}ms): {ex}")
            failed_models[model_name] = str(ex)

    # 4. Save results to docs/omega_api_probe_results.json
    results = {
        "provider": "Google Gemini",
        "api_key_masked": f"{API_KEY[:8]}...{API_KEY[-6:]}",
        "endpoint": "https://generativelanguage.googleapis.com/v1beta",
        "discovery_latency_ms": discovery_latency_ms,
        "total_models_available": len(models_list),
        "all_discovered_models": models_list,
        "tested_candidates": valid_candidates,
        "working_models": working_models,
        "failed_models": failed_models,
        "recommended_primary": working_models[0]["model"] if working_models else None,
        "timestamp": time.time()
    }
    with open("docs/omega_api_probe_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nExported probe results to docs/omega_api_probe_results.json with {len(working_models)} operational models.")

if __name__ == "__main__":
    main()
