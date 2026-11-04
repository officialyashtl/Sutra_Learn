"""
Testing suggested newer models:
gemini-3.8-flash, gemini-3.5-flash-lite, gemini-3.1-flash-lite, gemini-flash-lite-latest
"""
import urllib.request
import urllib.error
import json
import ssl
import time

API_KEY = "AQ.Ab8...fiVQ [REDACTED_FOR_SECURITY]"

candidates = [
    "gemini-flash-lite-latest",
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-3-flash-preview"
]

ctx = ssl.create_default_context()
for model in candidates:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": "Explain linear equations in one sentence."}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 100}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "SutraLearn-Omega/1.0"},
        method="POST"
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            dt = round((time.time() - t0) * 1000, 2)
            parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])
            text = parts[0].get("text", "").strip() if parts else ""
            print(f"[PASS] {model}: {dt}ms | Excerpt: {text[:80]}")
    except urllib.error.HTTPError as e:
        dt = round((time.time() - t0) * 1000, 2)
        print(f"[FAIL] {model}: HTTP {e.code} in {dt}ms: {e.read().decode('utf-8', errors='replace')[:100]}")
    except Exception as ex:
        print(f"[FAIL] {model}: Exception: {ex}")

