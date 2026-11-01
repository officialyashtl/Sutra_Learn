# SUTRA LEARN — AI Backend Pipeline Verification Probe
# Tests FastAPI /api/v1/ai/health, /api/v1/ai/providers, and /api/v1/ai/tutor endpoints using TestClient.

Write-Host '======================================================================' -ForegroundColor Cyan
Write-Host 'SUTRA LEARN — AI BACKEND PIPELINE PROBE' -ForegroundColor Cyan
Write-Host '======================================================================' -ForegroundColor Cyan

$outputJson = python scripts/ai/internal_verify_backend.py

if ($LASTEXITCODE -eq 0) {
    $result = $outputJson | ConvertFrom-Json
    Write-Host '[PASS] Health & Providers Endpoints: 200 OK' -ForegroundColor Green
    Write-Host '[PASS] Tutor Orchestration: 200 OK' -ForegroundColor Green
    Write-Host ('  Request ID:        ' + $result.request_id) -ForegroundColor Gray
    Write-Host ('  Selected Provider: ' + $result.selected_provider) -ForegroundColor Gray
    Write-Host ('  Selected Model:    ' + $result.selected_model) -ForegroundColor Gray
    Write-Host ('  Validation:        ' + $result.validation_status) -ForegroundColor Gray
    Write-Host ('  Latency:           ' + $result.latency_ms + ' ms') -ForegroundColor Gray
    Write-Host '======================================================================' -ForegroundColor Cyan
    Write-Host 'AI BACKEND PIPELINE VERIFICATION: SUCCESS (Exit Code 0)' -ForegroundColor Green
    exit 0
} else {
    Write-Host ('[FAIL] AI Backend Pipeline verification failed: ' + $outputJson) -ForegroundColor Red
    exit 1
}
