# SUTRA LEARN — Google Gemini Provider Verification Probe
# Validates API key authentication, model discovery, and error classification.

Write-Host '======================================================================' -ForegroundColor Cyan
Write-Host 'SUTRA LEARN — GOOGLE GEMINI PROVIDER PROBE' -ForegroundColor Cyan
Write-Host '======================================================================' -ForegroundColor Cyan

$pyScript = 'import os, sys, json; sys.path.insert(0, \"backend\"); from app.ai.config import get_ai_settings; from google import genai; settings = get_ai_settings(); key = settings.gemini_api_key;
if not key:
    print(json.dumps({\"status\": \"UNCONFIGURED\", \"message\": \"GEMINI_API_KEY is not configured\"}))
    sys.exit(0)
try:
    client = genai.Client(api_key=key)
    models = list(client.models.list())
    gemini_models = [m.name for m in models if \"gemini\" in m.name.lower()]
    print(json.dumps({\"status\": \"AUTHENTICATED\", \"models_available_count\": len(gemini_models), \"sample_models\": gemini_models[:3]}))
except Exception as e:
    print(json.dumps({\"status\": \"HANDSHAKE_ERROR\", \"error\": str(e)}))
'

$outputJson = python -c $pyScript
$result = $outputJson | ConvertFrom-Json

if ($result.status -eq 'AUTHENTICATED') {
    Write-Host '[PASS] Google Gemini API Authentication: SUCCESS' -ForegroundColor Green
    Write-Host ('[PASS] Available Gemini Models: ' + $result.models_available_count) -ForegroundColor Green
    Write-Host ('Sample Models: ' + ($result.sample_models -join ', ')) -ForegroundColor Gray
    Write-Host '======================================================================' -ForegroundColor Cyan
    Write-Host 'GEMINI PROVIDER PROBE: SUCCESS (Exit Code 0)' -ForegroundColor Green
    exit 0
} elseif ($result.status -eq 'UNCONFIGURED') {
    Write-Host '[WARN] Google Gemini API Key is not configured in .env' -ForegroundColor Yellow
    exit 0
} else {
    Write-Host ('[FAIL] Gemini handshake failed: ' + $result.error) -ForegroundColor Red
    exit 1
}
