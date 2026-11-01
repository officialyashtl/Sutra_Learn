# SUTRA LEARN — Qwen 3.5 4B Verification Probe
# Executes real mathematical inference against qwen3.5:4b.

Write-Host '======================================================================' -ForegroundColor Cyan
Write-Host 'SUTRA LEARN — QWEN 3.5 4B INFERENCE VERIFICATION' -ForegroundColor Cyan
Write-Host '======================================================================' -ForegroundColor Cyan

$baseUrl = 'http://127.0.0.1:11434'
$model = 'qwen3.5:4b'

$body = @{
    model = $model
    messages = @(
        @{
            role = 'user'
            content = 'State the first step to solve 3x + 6 = 21 in 10 words or less.'
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
    if (-not $content -and $res.message.thinking) {
        $subLen = [Math]::Min(120, $res.message.thinking.Length)
        $content = 'Thinking output generated: ' + $res.message.thinking.Substring(0, $subLen)
    }

    Write-Host ('[PASS] Model: ' + $res.model) -ForegroundColor Green
    Write-Host ('[PASS] Generation Latency: ' + $sw.ElapsedMilliseconds + ' ms') -ForegroundColor Green
    Write-Host ('[PASS] Tokens Evaluated: ' + $res.eval_count) -ForegroundColor Green
    Write-Host ('Output: ' + $content) -ForegroundColor Gray

    Write-Host '======================================================================' -ForegroundColor Cyan
    Write-Host 'QWEN 3.5 4B VERIFICATION: SUCCESS (Exit Code 0)' -ForegroundColor Green
    exit 0
} catch {
    $sw.Stop()
    Write-Host ('[FAIL] Inference failed: ' + $_) -ForegroundColor Red
    Write-Host ('Elapsed: ' + $sw.ElapsedMilliseconds + ' ms') -ForegroundColor Red
    exit 1
}
