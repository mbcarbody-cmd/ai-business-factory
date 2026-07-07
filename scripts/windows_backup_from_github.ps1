# Windows backup from GitHub for AI Business Factory
# Run in PowerShell.

$ErrorActionPreference = "Stop"

$backupRoot = "C:\AI_FACTORY_BACKUP"
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$repoUrl = "https://github.com/mbcarbody-cmd/ai-business-factory.git"
$repoDir = Join-Path $backupRoot "ai-business-factory"
$archiveDir = Join-Path $backupRoot "archives"

New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
New-Item -ItemType Directory -Force -Path $archiveDir | Out-Null

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Host "Git is not installed. Install Git for Windows first: https://git-scm.com/download/win" -ForegroundColor Red
  exit 1
}

if (Test-Path $repoDir) {
  Write-Host "Updating existing repo..."
  git -C $repoDir fetch --all --tags --prune
  git -C $repoDir pull --ff-only
} else {
  Write-Host "Cloning repo..."
  git clone $repoUrl $repoDir
}

$bundle = Join-Path $archiveDir "ai-business-factory-$stamp.bundle"
$zip = Join-Path $archiveDir "ai-business-factory-working-tree-$stamp.zip"

Write-Host "Creating portable git bundle..."
git -C $repoDir bundle create $bundle --all

Write-Host "Creating working tree zip..."
Compress-Archive -Path (Join-Path $repoDir "*") -DestinationPath $zip -Force

Write-Host "Backup complete:"
Write-Host "Repo:   $repoDir"
Write-Host "Bundle: $bundle"
Write-Host "Zip:    $zip"
Write-Host ""
Write-Host "Next: run scripts/windows_run_local.ps1 from inside the repo."
