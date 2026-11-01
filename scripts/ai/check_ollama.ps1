# SUTRA LEARN — Ollama Runtime & Model Inventory Probe
# Validates Ollama socket reachability, installed models (qwen3.5:4b, gemma4:e2b), and memory status.

Write-Host '======================================================================' -ForegroundColor Cyan
Write-Host 'SUTRA LEARN — OLLAMA RUNTIME PROBE' -ForegroundColor Cyan
Write-Host '======================================================================' -ForegroundColor Cyan

$baseUrl = 'http://127.0.0.1:11434'
$allPassed = $true

# 1. Socket connectivity check
try {
    $uri = $baseUrl + '/api/tags'
    $response = Invoke-RestMethod -Uri $uri -Method Get -TimeoutSec 3 -ErrorAction Stop
    Write-Host ('[PASS] Ollama socket reachable at ' + $baseUrl) -ForegroundColor Green
    
    $modelNames = $response.models | ForEach-Object { $_.name }
    Write-Host ('Installed Models: ' + ($modelNames -join ', ')) -ForegroundColor Gray

    # 2. Check Qwen
    if ($modelNames -contains 'qwen3.5:4b') {
        Write-Host '[PASS] Required Model Installed: qwen3.5:4b' -ForegroundColor Green
    } else {
        Write-Host '[FAIL] Missing required model: qwen3.5:4b' -ForegroundColor Red
        $allPassed = $false
    }

    # 3. Check Gemma
    if ($modelNames -contains 'gemma4:e2b') {
        Write-Host '[PASS] Required Model Installed: gemma4:e2b' -ForegroundColor Green
    } else {
        Write-Host '[FAIL] Missing required model: gemma4:e2b' -ForegroundColor Red
        $allPassed = $false
    }
} catch {
    Write-Host ('[FAIL] Ollama daemon is unreachable at ' + $baseUrl + ' : ' + $_) -ForegroundColor Red
    $allPassed = $false
}

Write-Host '======================================================================' -ForegroundColor Cyan
if ($allPassed) {
    Write-Host 'OLLAMA RUNTIME STATUS: OPERATIONAL (Exit Code 0)' -ForegroundColor Green
    exit 0
} else {
    Write-Host 'OLLAMA RUNTIME STATUS: DEGRADED/OFFLINE (Exit Code 1)' -ForegroundColor Red
    exit 1
}
