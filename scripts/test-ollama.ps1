# Test script for calling the local Ollama proxy endpoint
# Reads SERVICE_API_KEY from environment or .env and posts a sample prompt

$serviceKey = $env:SERVICE_API_KEY
if (-not $serviceKey -and (Test-Path .env)) {
  $content = Get-Content .env
  foreach ($line in $content) {
    if ($line -match '^\s*SERVICE_API_KEY\s*=\s*(.+)\s*$') {
      $serviceKey = $Matches[1].Trim('"')
      break
    }
  }
}

if (-not $serviceKey) { Write-Host "Warning: SERVICE_API_KEY not set. Requests may be unauthorized." }

$body = @{ prompt = "Summarize this text." } | ConvertTo-Json

Write-Host "Calling http://127.0.0.1:8000/api/ollama/generate..."
try {
  $resp = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/ollama/generate" -Method Post -ContentType "application/json" -Headers @{ 'x-api-key' = $serviceKey } -Body $body -ErrorAction Stop
  Write-Host "Response:`n" ($resp | ConvertTo-Json -Depth 5)
} catch {
  Write-Host "Request failed:`n" $_.Exception.Response.Content.ReadAsStringAsync().Result
}
