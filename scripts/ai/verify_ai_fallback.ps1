# SUTRA LEARN — AI Fallback & Mathematical Grounding Probe
# Tests deterministic curriculum engine failover and mathematical step verification.

Write-Host '======================================================================' -ForegroundColor Cyan
Write-Host 'SUTRA LEARN — DETERMINISTIC FALLBACK & MATHEMATICAL VERIFICATION' -ForegroundColor Cyan
Write-Host '======================================================================' -ForegroundColor Cyan

$outputJson = python scripts/ai/internal_verify_fallback.py

if ($LASTEXITCODE -eq 0) {
    $result = $outputJson | ConvertFrom-Json
    Write-Host '[PASS] Deterministic Fallback Generation: SUCCESS' -ForegroundColor Green
    Write-Host '[PASS] Mathematical Transformation Validation: VALID' -ForegroundColor Green
    Write-Host ('  Reason: ' + $result.validation_reason) -ForegroundColor Gray
    Write-Host ('  Hints:  ' + $result.hints_count + ' progressive hints supplied') -ForegroundColor Gray
    Write-Host '======================================================================' -ForegroundColor Cyan
    Write-Host 'AI FALLBACK & MATHEMATICAL VERIFICATION: SUCCESS (Exit Code 0)' -ForegroundColor Green
    exit 0
} else {
    Write-Host ('[FAIL] AI Fallback verification failed: ' + $outputJson) -ForegroundColor Red
    exit 1
}
