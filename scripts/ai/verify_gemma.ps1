# SUTRA LEARN — Gemma 4 E2B Verification Probe
# Executes real mathematical inference against gemma4:e2b.

Write-Host '======================================================================' -ForegroundColor Cyan
Write-Host 'SUTRA LEARN — GEMMA 4 E2B INFERENCE VERIFICATION' -ForegroundColor Cyan
Write-Host '======================================================================' -ForegroundColor Cyan

$baseUrl = 'http://127.0.0.1:11434'
$model = 'gemma4:e2b'

$body = @{
    model = $model
    messages = @(
        @{
            role = 'user'
            content = 'State the first step to solve 4x - 8 = 16 in 10 words or less.'
        }
    )
    stream = $false
    options = @{
        num_predict = 150
        temperature = 0.2
    }
} | ConvertTo-Json -Depth 5

$sw = [System.Diagnostics.Stopwatch]::StartNew()
try {
    $uri = $baseUrl + '/api/chat'
    $res = Invoke-RestMethod -Uri $uri -Method Post -Body $body -ContentType 'application/json' -TimeoutSec 180 -ErrorAction Stop
    $sw.Stop()

    $content = $res.message.content

    Write-Host ('[PASS] Model: ' + $res.model) -ForegroundColor Green
    Write-Host ('[PASS] Generation Latency: ' + $sw.ElapsedMilliseconds + ' ms') -ForegroundColor Green
    Write-Host ('[PASS] Tokens Evaluated: ' + $res.eval_count) -ForegroundColor Green
    Write-Host ('Output: ' + $content) -ForegroundColor Gray

    Write-Host '======================================================================' -ForegroundColor Cyan
    Write-Host 'GEMMA 4 E2B VERIFICATION: SUCCESS (Exit Code 0)' -ForegroundColor Green
    exit 0
} catch {
    $sw.Stop()
    Write-Host ('[FAIL] Inference failed: ' + $_) -ForegroundColor Red
    Write-Host ('Elapsed: ' + $sw.ElapsedMilliseconds + ' ms') -ForegroundColor Red
    exit 1
}
