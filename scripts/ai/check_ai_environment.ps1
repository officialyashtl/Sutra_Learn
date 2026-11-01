# SUTRA LEARN — AI Environment Diagnostic Script
# Verifies Python, required libraries, and non-sensitive configuration settings.

Write-Host '======================================================================' -ForegroundColor Cyan
Write-Host 'SUTRA LEARN — AI ENVIRONMENT DIAGNOSTIC PROBE' -ForegroundColor Cyan
Write-Host '======================================================================' -ForegroundColor Cyan

$allPassed = $true

# 1. Python check
try {
    $pyVer = python -c 'import sys; print(sys.version.split()[0])'
    Write-Host ('[PASS] Python Version: ' + $pyVer) -ForegroundColor Green
} catch {
    Write-Host '[FAIL] Python not accessible in PATH' -ForegroundColor Red
    $allPassed = $false
}

# 2. Package checks
$packages = @('fastapi', 'pydantic_settings', 'httpx', 'google.genai')
foreach ($pkg in $packages) {
    try {
        python -c ('import ' + $pkg) 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host ('[PASS] Library available: ' + $pkg) -ForegroundColor Green
        } else {
            Write-Host ('[WARN] Library missing in main environment: ' + $pkg) -ForegroundColor Yellow
        }
    } catch {
        Write-Host ('[WARN] Library check failed: ' + $pkg) -ForegroundColor Yellow
    }
}

# 3. Environment configuration check
$envPath = 'backend/.env'
if (Test-Path $envPath) {
    Write-Host ('[PASS] Configuration file found at ' + $envPath) -ForegroundColor Green
} else {
    Write-Host ('[WARN] ' + $envPath + ' not found') -ForegroundColor Yellow
}

# 4. Settings verification via Pydantic
$pyCmd = 'import sys, json; sys.path.insert(0, \"backend\"); from app.ai.config import get_ai_settings; print(json.dumps(get_ai_settings().get_safe_status()))'
try {
    $safeStatus = python -c $pyCmd
    if ($LASTEXITCODE -eq 0) {
        Write-Host '[PASS] AISettings loaded and validated successfully' -ForegroundColor Green
        Write-Host ('Safe Telemetry: ' + $safeStatus) -ForegroundColor Gray
    } else {
        Write-Host '[FAIL] Failed to load AISettings' -ForegroundColor Red
        $allPassed = $false
    }
} catch {
    Write-Host ('[FAIL] Exception evaluating AISettings: ' + $_) -ForegroundColor Red
    $allPassed = $false
}

Write-Host '======================================================================' -ForegroundColor Cyan
if ($allPassed) {
    Write-Host 'AI ENVIRONMENT STATUS: READY (Exit Code 0)' -ForegroundColor Green
    exit 0
} else {
    Write-Host 'AI ENVIRONMENT STATUS: ISSUES DETECTED (Exit Code 1)' -ForegroundColor Red
    exit 1
}
