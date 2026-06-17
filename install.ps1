# summarize skill — one-line installer (Windows PowerShell)
# iwr https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/install.ps1 | iex

$ErrorActionPreference = "Stop"

$InstallDir = "$env:USERPROFILE\.agent-skills\summarize"
$RepoSSH   = "git@github.com:gtbwpkwjnb-alt/summarize-skill.git"
$RepoHTTPS = "https://github.com/gtbwpkwjnb-alt/summarize-skill.git"

Write-Host "📦 summarize skill installer"

if (Test-Path $InstallDir) {
    Write-Host "   Already installed at $InstallDir"
    Write-Host "🔄 Updating to latest version..."
    Push-Location $InstallDir
    try {
        git pull --rebase 2>$null
    } catch {
        Pop-Location
        Remove-Item -Recurse -Force $InstallDir -ErrorAction SilentlyContinue
        try { git clone $RepoSSH $InstallDir } catch { git clone $RepoHTTPS $InstallDir }
    }
    Pop-Location
} else {
    Write-Host "   Cloning into $InstallDir ..."
    New-Item -ItemType Directory -Force -Path (Split-Path $InstallDir) | Out-Null
    try { git clone $RepoSSH $InstallDir } catch { git clone $RepoHTTPS $InstallDir }
}

$ver = Get-Content "$InstallDir\VERSION" -Raw
Write-Host ""
Write-Host "✅ summarize skill installed!  v$ver"
Write-Host "   Path:    $InstallDir"
Write-Host "   Trigger: /总结"
Write-Host ""
Write-Host "📊 Manage:"
Write-Host "   Update:  cd $InstallDir; git pull"
Write-Host "   Issues:  https://github.com/gtbwpkwjnb-alt/summarize-skill/issues"
