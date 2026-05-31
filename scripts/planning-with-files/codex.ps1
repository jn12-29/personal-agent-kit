Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoUrl = "https://github.com/OthmanAdi/planning-with-files.git"
$tempDir = Join-Path $env:TEMP "planning-with-files"
$codexDir = Join-Path $HOME ".codex"
$skillDestination = Join-Path $codexDir "skills"
$hooksDestination = Join-Path $codexDir "hooks"

if (Test-Path -LiteralPath $tempDir) {
    Remove-Item -LiteralPath $tempDir -Recurse -Force
}

git clone $repoUrl $tempDir
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

New-Item -ItemType Directory -Path $skillDestination -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $tempDir ".codex/skills/planning-with-files") -Destination $skillDestination -Recurse -Force

New-Item -ItemType Directory -Path $hooksDestination -Force | Out-Null
Copy-Item -Path (Join-Path $tempDir ".codex/hooks/*") -Destination $hooksDestination -Recurse -Force

Write-Output "If you already have ~/.codex/hooks.json, merge the planning-with-files entries manually."
Copy-Item -LiteralPath (Join-Path $tempDir ".codex/hooks.json") -Destination (Join-Path $codexDir "hooks.json") -Force

Remove-Item -LiteralPath $tempDir -Recurse -Force
