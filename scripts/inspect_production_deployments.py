import httpx
import re
import json

print("=== CHECKING VERCEL PRODUCTION DEPLOYMENT ===")
try:
    resp = httpx.get("https://sutralearn.vercel.app/", timeout=15)
    print("Vercel Index Status:", resp.status_code)
    scripts = re.findall(r'src=["\']([^"\']+\.js)["\']', resp.text)
    print("Script tags found:", scripts)
    for s in scripts:
        url = f"https://sutralearn.vercel.app{s}" if s.startswith("/") else s
        js_resp = httpx.get(url, timeout=15)
        print(f"Bundle {s}: {len(js_resp.content)} bytes, status {js_resp.status_code}")
        
        # Check for our recent changes
        has_new_title = "SUTRA AI • GROUNDED TUTOR" in js_resp.text
        has_sutra_loader = "SutraPageLoader" in js_resp.text or "sutra-spin" in js_resp.text
        has_old_badge = "Google Gemini (gemini-flash-lite-latest)" in js_resp.text
        print(f"  Contains 'SUTRA AI • GROUNDED TUTOR': {has_new_title}")
        print(f"  Contains SUTRA loaders: {has_sutra_loader}")
        print(f"  Contains old provider badge text: {has_old_badge}")
except Exception as e:
    print("Vercel check error:", e)

print("\n=== CHECKING RENDER PRODUCTION DEPLOYMENT ===")
try:
    r_health = httpx.get("https://sutra-learn-api.onrender.com/api/v1/health", timeout=15)
    print("Render Health:", r_health.status_code, r_health.json())
    
    r_ai = httpx.get("https://sutra-learn-api.onrender.com/api/v1/ai/health", timeout=15)
    print("Render AI Health Status:", r_ai.status_code)
    ai_data = r_ai.json()
    print("Operating Mode:", ai_data.get("operating_mode"))
    gemini_prov = next((p for p in ai_data.get("providers", []) if p.get("provider_id") == "gemini"), None)
    if gemini_prov:
        print("Gemini Provider Info:")
        print("  Configured:", gemini_prov.get("configured"))
        print("  Enabled:", gemini_prov.get("enabled"))
        print("  Model ID:", gemini_prov.get("model_id"))
        print("  Health Status:", gemini_prov.get("health_status"))
        print("  Circuit State:", gemini_prov.get("circuit_state"))
    else:
        print("Gemini provider not found in AI health!")
except Exception as e:
    print("Render check error:", e)
