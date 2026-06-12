Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoUrl = "https://github.com/OthmanAdi/planning-with-files.git"
$targetProject = (Get-Location).Path
$codexDir = Join-Path $targetProject ".codex"
$tempRoot = if ($env:TEMP) { $env:TEMP } else { [System.IO.Path]::GetTempPath() }
$tempDir = Join-Path $tempRoot "planning-with-files-$([guid]::NewGuid().ToString('N'))"

function Backup-Path {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (Test-Path -LiteralPath $Path) {
        $backup = "$Path.bak.$(Get-Date -Format 'yyyyMMddHHmmss')"
        Move-Item -LiteralPath $Path -Destination $backup
        Write-Output "Backed up: $Path -> $backup"
    }
}

function Copy-DirectoryReplacing {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Source,
        [Parameter(Mandatory = $true)]
        [string]$Destination
    )

    Backup-Path $Destination
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    Get-ChildItem -LiteralPath $Source -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $Destination -Recurse -Force
    }
}

function Copy-FileReplacing {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Source,
        [Parameter(Mandatory = $true)]
        [string]$Destination
    )

    Backup-Path $Destination
    $parent = Split-Path -Parent $Destination
    if ($parent) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
}

function Copy-EntryReplacing {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Source,
        [Parameter(Mandatory = $true)]
        [string]$Destination
    )

    $item = Get-Item -LiteralPath $Source -Force
    if ($item.PSIsContainer) {
        Copy-DirectoryReplacing $Source $Destination
    } else {
        Copy-FileReplacing $Source $Destination
    }
}

try {
    git clone --depth 1 $repoUrl $tempDir
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    New-Item -ItemType Directory -Path (Join-Path $codexDir "skills") -Force | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $codexDir "hooks") -Force | Out-Null

    Copy-DirectoryReplacing `
        (Join-Path $tempDir ".codex/skills/planning-with-files") `
        (Join-Path $codexDir "skills/planning-with-files")

    $sourceHooks = Join-Path $tempDir ".codex/hooks"
    $targetHooks = Join-Path $codexDir "hooks"
    Get-ChildItem -LiteralPath $sourceHooks -Force | ForEach-Object {
        Copy-EntryReplacing $_.FullName (Join-Path $targetHooks $_.Name)
    }

    Copy-FileReplacing (Join-Path $tempDir ".codex/hooks.json") (Join-Path $codexDir "hooks.json")

    Write-Output "Installed planning-with-files for Codex in: $codexDir"
    Write-Output "Review and trust project hooks with /hooks when Codex prompts for hook trust."
} finally {
    if (Test-Path -LiteralPath $tempDir) {
        Remove-Item -LiteralPath $tempDir -Recurse -Force
    }
}
