# summarize skill — multi-platform one-line installer (Windows PowerShell)

$ErrorActionPreference = "Stop"

$RepoSSH   = "git@github.com:gtbwpkwjnb-alt/summarize-skill.git"
$RepoHTTPS = "https://github.com/gtbwpkwjnb-alt/summarize-skill.git"

# --- Platform auto-detect ---
function Get-InstallDir {
    # ZCode (默认 ~/.agents/skills/)
    if (Test-Path "$env:USERPROFILE\.agents\skills") {
        return "$env:USERPROFILE\.agents\skills\session-summarize"
    }
    # CodeBuddy
    if (Test-Path "$env:USERPROFILE\.codebuddy\skills") {
        return "$env:USERPROFILE\.codebuddy\skills\session-summarize"
    }
    # Claude Code
    if (Test-Path "$env:USERPROFILE\.claude\skills") {
        return "$env:USERPROFILE\.claude\skills\session-summarize"
    }
    # Codex
    if (Test-Path "$env:USERPROFILE\.codex\skills") {
        return "$env:USERPROFILE\.codex\skills\session-summarize"
    }
    # Reasonix
    if (Test-Path "$env:USERPROFILE\.reasonix\skills") {
        return "$env:USERPROFILE\.reasonix\skills\session-summarize"
    }
    # Fallback
    return "$env:USERPROFILE\.agent-skills\session-summarize"
}

$InstallDir = Get-InstallDir
$LegacyInstallDir = Join-Path (Split-Path $InstallDir -Parent) "summarize"

Write-Host "📦 Session Summarize installer"
Write-Host "   Target: $InstallDir"

if (-not (Test-Path $InstallDir) -and (Test-Path $LegacyInstallDir)) {
    Write-Host "   Migrating legacy install: $LegacyInstallDir"
    Move-Item -LiteralPath $LegacyInstallDir -Destination $InstallDir
}

if (Test-Path $InstallDir) {
    Write-Host "   Already installed at $InstallDir"
    Write-Host "🔄 Updating to latest version..."
    Push-Location $InstallDir
    try {
        git pull --ff-only
        if ($LASTEXITCODE -ne 0) {
            throw "git pull --ff-only failed; existing installation was preserved"
        }
    } finally {
        Pop-Location
    }
} else {
    Write-Host "   Cloning into $InstallDir ..."
    New-Item -ItemType Directory -Force -Path (Split-Path $InstallDir) | Out-Null
    git clone $RepoSSH $InstallDir
    if ($LASTEXITCODE -ne 0) {
        git clone $RepoHTTPS $InstallDir
        if ($LASTEXITCODE -ne 0) {
            throw "git clone failed"
        }
    }
}

$ver = Get-Content "$InstallDir\VERSION" -Raw
Write-Host ""
Write-Host "✅ summarize skill installed!  v$ver"
Write-Host "   Path:    $InstallDir"
Write-Host "   Trigger: 总结 / session-summarize / summarize"
Write-Host ""
Write-Host "📊 Manage:"
Write-Host "   Update:  cd $InstallDir; git pull"
Write-Host "   Issues:  https://github.com/gtbwpkwjnb-alt/summarize-skill/issues"
