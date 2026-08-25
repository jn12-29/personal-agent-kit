Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = if ($env:AGENT_KIT_DIR) {
    $env:AGENT_KIT_DIR
} else {
    [System.IO.Path]::GetFullPath((Join-Path $scriptDir ".."))
}
$codexInstallDir = if ($env:CODEX_HOME) {
    $env:CODEX_HOME
} else {
    Join-Path $HOME ".codex"
}

function Resolve-FullPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    return [System.IO.Path]::GetFullPath($Path)
}

function Backup-Path {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [ref]$BackupPath,
        [string]$BackupDirectory
    )

    $BackupPath.Value = $null

    if (-not (Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue)) {
        return
    }

    if ($BackupDirectory) {
        New-Item -ItemType Directory -Path $BackupDirectory -Force | Out-Null
        $backupName = "$(Split-Path -Leaf $Path).bak.$(Get-Date -Format 'yyyyMMddHHmmss')"
        $backup = Join-Path $BackupDirectory $backupName
    } else {
        $backup = "$Path.bak.$(Get-Date -Format 'yyyyMMddHHmmss')"
    }
    Move-Item -LiteralPath $Path -Destination $backup
    $BackupPath.Value = $backup
    Write-Output "Backed up: $Path -> $backup"
}

function Remove-InstalledPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if (-not $item) {
        return
    }

    if ($item.LinkType) {
        if ($item.PSIsContainer) {
            [System.IO.Directory]::Delete($item.FullName)
        } else {
            [System.IO.File]::Delete($item.FullName)
        }
        return
    }

    if ($item.PSIsContainer) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    } else {
        Remove-Item -LiteralPath $Path -Force
    }
}

function Restore-Backup {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [string]$BackupPath
    )

    Remove-InstalledPath $Path

    if (-not $BackupPath) {
        return
    }

    Move-Item -LiteralPath $BackupPath -Destination $Path
    Write-Output "Restored backup: $Path <- $BackupPath"
}

function Request-Confirmation {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Question
    )

    while ($true) {
        try {
            $answer = Read-Host "$Question [y/N]"
        } catch {
            Write-Output "Fallback requires confirmation, but interactive input is unavailable."
            return $false
        }

        switch ($answer.Trim().ToLowerInvariant()) {
            "y" { return $true }
            "yes" { return $true }
            "" { return $false }
            "n" { return $false }
            "no" { return $false }
            default { Write-Output "Please answer y or n." }
        }
    }
}

function Test-LinkedTarget {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Source,
        [Parameter(Mandatory = $true)]
        [string]$Destination
    )

    if (-not (Test-Path -LiteralPath $Destination)) {
        return $false
    }

    $item = Get-Item -LiteralPath $Destination -Force
    if (-not $item.LinkType -or -not $item.Target) {
        return $false
    }

    $target = $item.Target
    if ($target -is [System.Array]) {
        $target = $target[0]
    }

    return (Resolve-FullPath $Source) -eq (Resolve-FullPath $target)
}

function Install-LinkOrCopy {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Source,
        [Parameter(Mandatory = $true)]
        [string]$Destination,
        [string]$BackupDirectory
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        Write-Output "Missing source, skipped: $Source"
        return
    }

    $destinationDir = Split-Path -Parent $Destination
    if ($destinationDir) {
        New-Item -ItemType Directory -Path $destinationDir -Force | Out-Null
    }

    if (Test-LinkedTarget $Source $Destination) {
        Write-Output "Already linked: $Destination"
        return
    }

    $backupPath = $null
    Backup-Path $Destination ([ref]$backupPath) $BackupDirectory

    $sourceItem = Get-Item -LiteralPath $Source -Force
    $sourceIsDirectory = $sourceItem.PSIsContainer

    try {
        New-Item -ItemType SymbolicLink -Path $Destination -Value $Source -Force | Out-Null
        Write-Output "Linked with symlink: $Destination -> $Source"
        return
    } catch {
        Write-Output "Symbolic link failed: $Destination -> $Source"
        Write-Output "Reason: $($_.Exception.Message)"
    }

    try {
        if ($sourceIsDirectory) {
            if (Request-Confirmation "Use a junction fallback for $Destination") {
                try {
                    New-Item -ItemType Junction -Path $Destination -Value $Source -Force | Out-Null
                    Write-Output "Linked with junction: $Destination -> $Source"
                    return
                } catch {
                    Write-Output "Junction fallback failed: $($_.Exception.Message)"
                }
            } else {
                Write-Output "Junction fallback declined: $Destination"
            }
        } else {
            if (Request-Confirmation "Use a hard link fallback for $Destination") {
                try {
                    New-Item -ItemType HardLink -Path $Destination -Value $Source -Force | Out-Null
                    Write-Output "Linked with hard link: $Destination -> $Source"
                    return
                } catch {
                    Write-Output "Hard link fallback failed: $($_.Exception.Message)"
                }
            } else {
                Write-Output "Hard link fallback declined: $Destination"
            }
        }

        if (Request-Confirmation "Copy instead of linking $Destination") {
            if ($sourceIsDirectory) {
                Copy-Item -LiteralPath $Source -Destination $Destination -Recurse -Force
            } else {
                Copy-Item -LiteralPath $Source -Destination $Destination -Force
            }

            Write-Output "Copied instead of linking: $Destination <- $Source"
            return
        }

        Write-Output "Copy fallback declined: $Destination"
        throw "No approved fallback for $Destination"
    } catch {
        Restore-Backup $Destination $backupPath
        throw
    }
}

# Codex and OpenCode share the skills source at $repo/skills.
Install-LinkOrCopy (Join-Path $repo "skills") (Join-Path $HOME ".agents/skills")

# GLOBAL_AGENTS.md is installed into the supported tools' global instruction paths.
Install-LinkOrCopy (Join-Path $repo "GLOBAL_AGENTS.md") (Join-Path $codexInstallDir "AGENTS.md")
Install-LinkOrCopy (Join-Path $repo "GLOBAL_AGENTS.md") (Join-Path $HOME ".config/opencode/AGENTS.md")

Write-Output ""
Write-Output "Done. To install config files with backup:"
$configScript = Join-Path $repo "scripts/install-config.ps1"
Write-Output "  powershell -ExecutionPolicy Bypass -File `"$configScript`""
