param(
    [Parameter(Mandatory=$true)]
    [string]$Target,

    [switch]$Force,
    [switch]$DryRun,
    [switch]$InstallGlobalSkill,
    [string]$GlobalSkillTarget = (Join-Path $env:USERPROFILE ".codex\skills")
)

$ErrorActionPreference = "Stop"

$PackageRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$TargetPath = [System.IO.Path]::GetFullPath($Target)
$Stamp = Get-Date -Format "yyyyMMdd-HHmmss"

$Items = @(
    "AGENTS.md",
    "CODEX.md",
    "CLAUDE.md",
    ".codex-skills\procedural-verification-harness"
)

if (!(Test-Path -LiteralPath $TargetPath)) {
    throw "Target does not exist: $TargetPath"
}

function Install-Item {
    param([string]$RelativePath)

    $Source = Join-Path $PackageRoot $RelativePath
    $Destination = Join-Path $TargetPath $RelativePath
    $DestinationParent = Split-Path -Parent $Destination

    if (!(Test-Path -LiteralPath $Source)) {
        throw "Missing package item: $Source"
    }

    if (Test-Path -LiteralPath $Destination) {
        if (!$Force) {
            throw "Refusing to overwrite existing item without -Force: $Destination"
        }
        $Backup = "$Destination.bak.$Stamp"
        Write-Output "backup: $Destination -> $Backup"
        if (!$DryRun) {
            Copy-Item -LiteralPath $Destination -Destination $Backup -Recurse -Force
        }
    }

    Write-Output "install: $Source -> $Destination"
    if (!$DryRun) {
        New-Item -ItemType Directory -Force -Path $DestinationParent | Out-Null
        Copy-Item -LiteralPath $Source -Destination $Destination -Recurse -Force
    }
}

foreach ($Item in $Items) {
    Install-Item -RelativePath $Item
}

if ($InstallGlobalSkill) {
    $GlobalSkillRoot = [System.IO.Path]::GetFullPath($GlobalSkillTarget)
    $GlobalDestination = Join-Path $GlobalSkillRoot "procedural-verification-harness"
    $GlobalSource = Join-Path $PackageRoot ".codex-skills\procedural-verification-harness"

    if (Test-Path -LiteralPath $GlobalDestination) {
        if (!$Force) {
            throw "Refusing to overwrite existing global skill without -Force: $GlobalDestination"
        }
        $Backup = "$GlobalDestination.bak.$Stamp"
        Write-Output "backup: $GlobalDestination -> $Backup"
        if (!$DryRun) {
            Copy-Item -LiteralPath $GlobalDestination -Destination $Backup -Recurse -Force
        }
    }

    Write-Output "install global skill: $GlobalSource -> $GlobalDestination"
    if (!$DryRun) {
        New-Item -ItemType Directory -Force -Path $GlobalSkillRoot | Out-Null
        Copy-Item -LiteralPath $GlobalSource -Destination $GlobalDestination -Recurse -Force
    }
}

Write-Output "done"
