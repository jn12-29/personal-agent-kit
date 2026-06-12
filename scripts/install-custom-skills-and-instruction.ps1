Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = if ($env:AGENT_KIT_DIR) {
    $env:AGENT_KIT_DIR
} else {
    [System.IO.Path]::GetFullPath((Join-Path $scriptDir ".."))
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

function Ensure-RealDirectory {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $parent = Split-Path -Parent $Path
    if ($parent) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    if (Test-Path -LiteralPath $Path) {
        $item = Get-Item -LiteralPath $Path -Force
        if ($item.PSIsContainer -and -not $item.LinkType) {
            return
        }
    }

    $backupPath = $null
    Backup-Path $Path ([ref]$backupPath)
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
}

function Remove-StaleClaudeSkills {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SourceDirectory,
        [Parameter(Mandatory = $true)]
        [string]$DestinationDirectory
    )

    $separator = [string][System.IO.Path]::DirectorySeparatorChar
    $sourceRoot = Resolve-FullPath $SourceDirectory
    if (-not $sourceRoot.EndsWith($separator)) {
        $sourceRoot = "$sourceRoot$separator"
    }

    $comparison = if ([System.IO.Path]::DirectorySeparatorChar -eq "\") {
        [System.StringComparison]::OrdinalIgnoreCase
    } else {
        [System.StringComparison]::Ordinal
    }

    $items = Get-ChildItem -LiteralPath $DestinationDirectory -Force -ErrorAction SilentlyContinue
    foreach ($item in $items) {
        if ($item.LinkType -ne "SymbolicLink" -and $item.LinkType -ne "Junction") {
            continue
        }

        $target = $item.Target
        if ($target -is [System.Array]) {
            $target = $target[0]
        }
        if (-not $target) {
            continue
        }

        if ([System.IO.Path]::IsPathRooted($target)) {
            $targetPath = $target
        } else {
            $targetPath = Join-Path (Split-Path -Parent $item.FullName) $target
        }

        $targetFullPath = Resolve-FullPath $targetPath
        if (-not $targetFullPath.StartsWith($sourceRoot, $comparison)) {
            continue
        }

        if (Test-Path -LiteralPath $targetFullPath) {
            continue
        }

        Remove-InstalledPath $item.FullName
        Write-Output "Removed stale Claude skill link: $($item.FullName) -> $target"
    }
}

function Install-ClaudeSkills {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SourceDirectory,
        [Parameter(Mandatory = $true)]
        [string]$DestinationDirectory
    )

    if (-not (Test-Path -LiteralPath $SourceDirectory -PathType Container)) {
        Write-Output "Missing skills directory, skipped: $SourceDirectory"
        return
    }

    Ensure-RealDirectory $DestinationDirectory
    Remove-StaleClaudeSkills $SourceDirectory $DestinationDirectory

    $skills = Get-ChildItem -LiteralPath $SourceDirectory -Directory
    if (-not $skills) {
        Write-Output "No skill directories found: $SourceDirectory"
        return
    }

    foreach ($skill in $skills) {
        Install-LinkOrCopy $skill.FullName (Join-Path $DestinationDirectory $skill.Name) (Join-Path $HOME ".claude/skills-backups")
    }
}

Install-LinkOrCopy (Join-Path $repo "skills") (Join-Path $HOME ".agents/skills")
Install-ClaudeSkills (Join-Path $repo "skills") (Join-Path $HOME ".claude/skills")
Install-LinkOrCopy (Join-Path $repo "GLOBAL_AGENTS.md") (Join-Path $HOME ".codex/AGENTS.md")
Install-LinkOrCopy (Join-Path $repo "GLOBAL_AGENTS.md") (Join-Path $HOME ".config/opencode/AGENTS.md")
Install-LinkOrCopy (Join-Path $repo "GLOBAL_AGENTS.md") (Join-Path $HOME ".claude/CLAUDE.md")

Write-Output ""
Write-Output "Done. To install config files with backup:"
$configScript = Join-Path $repo "scripts/install-config.ps1"
Write-Output "  powershell -ExecutionPolicy Bypass -File `"$configScript`""
