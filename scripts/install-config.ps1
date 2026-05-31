Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = if ($env:AGENT_KIT_DIR) {
    $env:AGENT_KIT_DIR
} else {
    [System.IO.Path]::GetFullPath((Join-Path $scriptDir ".."))
}

function Copy-Config {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Source,
        [Parameter(Mandatory = $true)]
        [string]$Destination
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        Write-Output "Missing source, skipped: $Source"
        return
    }

    $destinationDir = Split-Path -Parent $Destination
    if ($destinationDir) {
        New-Item -ItemType Directory -Path $destinationDir -Force | Out-Null
    }

    if (Test-Path -LiteralPath $Destination) {
        $backup = "$Destination.bak.$(Get-Date -Format 'yyyyMMddHHmmss')"
        Move-Item -LiteralPath $Destination -Destination $backup
        Write-Output "Backed up: $Destination -> $backup"
    }

    Copy-Item -LiteralPath $Source -Destination $Destination
    Write-Output "Installed: $Destination <- $Source"
}

Copy-Config (Join-Path $repo "config/config.toml") (Join-Path $HOME ".codex/config.toml")
Copy-Config (Join-Path $repo "config/opencode.json") (Join-Path $HOME ".config/opencode/opencode.json")
