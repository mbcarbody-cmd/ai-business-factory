# Local Windows runner for AI Business Factory browser products
# Run from repository root in PowerShell:
# powershell -ExecutionPolicy Bypass -File scripts/windows_run_local.ps1

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$website = Join-Path $root "website"
$port = 8787

if (-not (Test-Path $website)) {
  Write-Host "website folder not found. Run this script from the cloned ai-business-factory repo." -ForegroundColor Red
  exit 1
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command py -ErrorAction SilentlyContinue }

if (-not $python) {
  Write-Host "Python not found. Install Python from Microsoft Store or python.org, then rerun." -ForegroundColor Red
  exit 1
}

Write-Host "Starting local server at http://localhost:$port"
Write-Host "Open product: http://localhost:$port/video-maker.html"
Write-Host "Android wrapper: http://localhost:$port/android.html"
Write-Host "QA harness: http://localhost:$port/video-maker-android-qa.html"
Write-Host "Proof intake: http://localhost:$port/quick-video-qa-proof-intake.html"
Write-Host "Press Ctrl+C to stop."

Set-Location $website
if ($python.Name -eq "py.exe") {
  py -m http.server $port
} else {
  python -m http.server $port
}
