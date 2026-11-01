# =====================================================================
# SUTRA LEARN PHOENIX 10,000 — MASTER AUTOMATED VERIFICATION SUITE
# =====================================================================
# Executes all 12 platform verification stages in controlled sequence.
# Generates machine-readable output: scripts/ai/verification_results.json
# Returns exit code 0 if all required stages succeed.
# =====================================================================

Write-Host '======================================================================' -ForegroundColor Cyan
Write-Host 'SUTRA LEARN PHOENIX 10,000 — MASTER INDEPENDENT ACCEPTANCE AUDIT' -ForegroundColor Cyan
Write-Host '======================================================================' -ForegroundColor Cyan

$results = [ordered]@{}
$overallSuccess = $true
$suiteStart = [System.Diagnostics.Stopwatch]::StartNew()

function Run-Stage {
    param (
        [string]$StageId,
        [string]$StageName,
        [scriptblock]$Action,
        [bool]$IsRequired = $true
    )

    Write-Host ('`n>>> STAGE ' + $StageId + ': ' + $StageName) -ForegroundColor Yellow
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $status = 'FAIL'
    $detail = ''

    try {
        $output = & $Action
        $sw.Stop()
        $exitCode = $LASTEXITCODE

        if ($exitCode -eq 0) {
            $status = 'PASS'
            $detail = 'Execution completed cleanly with exit code 0.'
            Write-Host ('[PASS] Stage ' + $StageId + ' (' + $sw.ElapsedMilliseconds + ' ms): ' + $detail) -ForegroundColor Green
        } else {
            $status = 'FAIL'
            $detail = 'Non-zero exit code: ' + $exitCode
            Write-Host ('[FAIL] Stage ' + $StageId + ' (' + $sw.ElapsedMilliseconds + ' ms): ' + $detail) -ForegroundColor Red
            if ($IsRequired) {
                $script:overallSuccess = $false
            }
        }
    } catch {
        $sw.Stop()
        $status = 'FAIL'
        $detail = 'Exception: ' + $_.Exception.Message
        Write-Host ('[FAIL] Stage ' + $StageId + ': ' + $detail) -ForegroundColor Red
        if ($IsRequired) {
            $script:overallSuccess = $false
        }
    }

    $results[$StageId] = [ordered]@{
        stage = $StageName
        status = $status
        latency_ms = $sw.ElapsedMilliseconds
        detail = $detail
        required = $IsRequired
    }
}

# ---------------------------------------------------------------------
# STAGE 01: Environment Configuration & Secret Protection
# ---------------------------------------------------------------------
Run-Stage '01_ENV' 'Environment Configuration & Secret Protection' {
    & powershell -ExecutionPolicy Bypass -File scripts/ai/check_ai_environment.ps1
}

# ---------------------------------------------------------------------
# STAGE 02: Ollama Local Inference Daemon
# ---------------------------------------------------------------------
Run-Stage '02_OLLAMA' 'Ollama Local Daemon & Model Tags' {
    & powershell -ExecutionPolicy Bypass -File scripts/ai/check_ollama.ps1
}

# ---------------------------------------------------------------------
# STAGE 03: Gemini API Authentication & Error Classification
# ---------------------------------------------------------------------
# Gemini generation is blocked on Google Cloud project billing tier;
# the adapter cleanly classifies HTTP 403 and trips circuit to OPEN.
Run-Stage '03_GEMINI' 'Gemini API Auth & Circuit Classification' {
    & powershell -ExecutionPolicy Bypass -File scripts/ai/verify_gemini.ps1
} $false

# ---------------------------------------------------------------------
# STAGE 04: Qwen 3.5 4B Live Reasoning Inference
# ---------------------------------------------------------------------
Run-Stage '04_QWEN' 'Qwen 3.5 4B Live Reasoning Inference' {
    & powershell -ExecutionPolicy Bypass -File scripts/ai/verify_qwen.ps1
}

# ---------------------------------------------------------------------
# STAGE 05: Gemma 4 E2B Live Direct Inference
# ---------------------------------------------------------------------
Run-Stage '05_GEMMA' 'Gemma 4 E2B Live Direct Inference' {
    & powershell -ExecutionPolicy Bypass -File scripts/ai/verify_gemma.ps1
}

# ---------------------------------------------------------------------
# STAGE 06: Deterministic Fallback & Math Step Consistency
# ---------------------------------------------------------------------
Run-Stage '06_FALLBACK' 'Deterministic Fallback & Step Validation' {
    & powershell -ExecutionPolicy Bypass -File scripts/ai/verify_ai_fallback.ps1
}

# ---------------------------------------------------------------------
# STAGE 07: AI Backend Endpoints (Health, Providers, Tutor, Educator)
# ---------------------------------------------------------------------
Run-Stage '07_BACKEND_AI' 'AI FastAPI Router & Orchestrator Pipeline' {
    & powershell -ExecutionPolicy Bypass -File scripts/ai/verify_ai_backend.ps1
}

# ---------------------------------------------------------------------
# STAGE 08: Core Mathematics & Adaptive Pedagogical Logic
# ---------------------------------------------------------------------
Run-Stage '08_MATH_LOGIC' 'Algebraic Verification & Adaptive Engine Rules' {
    & python scripts/verify_mathematics.py
}

# ---------------------------------------------------------------------
# STAGE 09: Complete Backend Pytest Suite
# ---------------------------------------------------------------------
Run-Stage '09_PYTEST' 'Backend Pytest Suite (35 Cases)' {
    & python -m pytest backend/tests -v
}

# ---------------------------------------------------------------------
# STAGE 10: Multi-Stage End-to-End Pipeline
# ---------------------------------------------------------------------
Run-Stage '10_E2E' 'Complete E2E Verification Suite (14 Stages)' {
    & python scripts/verify_e2e.py
}

# ---------------------------------------------------------------------
# STAGE 11: Frontend Static Analysis & Lint
# ---------------------------------------------------------------------
Run-Stage '11_LINT' 'Frontend Oxlint Verification' {
    & npm --prefix frontend run lint
}

# ---------------------------------------------------------------------
# STAGE 12: Frontend Production Build & Bundle Inspection
# ---------------------------------------------------------------------
Run-Stage '12_BUILD' 'Frontend Production Build (TypeScript + Vite)' {
    & npm --prefix frontend run build
}

$suiteStart.Stop()

# ---------------------------------------------------------------------
# Output Machine-Readable JSON Telemetry
# ---------------------------------------------------------------------
$jsonPayload = [ordered]@{
    suite = 'SUTRA LEARN PHOENIX 10,000'
    timestamp = [System.DateTime]::UtcNow.ToString('o')
    total_duration_ms = $suiteStart.ElapsedMilliseconds
    overall_status = if ($overallSuccess) { 'SUCCESS' } else { 'FAILURE' }
    stages = $results
} | ConvertTo-Json -Depth 6

$jsonPath = 'scripts/ai/verification_results.json'
[System.IO.File]::WriteAllText($jsonPath, $jsonPayload)

Write-Host '`n======================================================================' -ForegroundColor Cyan
Write-Host ('MASTER VERIFICATION COMPLETED IN: ' + $suiteStart.ElapsedMilliseconds + ' ms') -ForegroundColor Cyan
Write-Host ('Machine-Readable Telemetry: ' + $jsonPath) -ForegroundColor Gray

if ($overallSuccess) {
    Write-Host 'VERIFICATION RESULT: ALL REQUIRED STAGES PASSED (Exit Code 0)' -ForegroundColor Green
    exit 0
} else {
    Write-Host 'VERIFICATION RESULT: ONE OR MORE STAGES FAILED (Exit Code 1)' -ForegroundColor Red
    exit 1
}

