#!/bin/bash
# summarize skill — multi-platform one-line installer
# curl -sL https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/scripts/install.sh | bash

set -e

REPO_SSH="git@github.com:gtbwpkwjnb-alt/summarize-skill.git"
REPO_HTTPS="https://github.com/gtbwpkwjnb-alt/summarize-skill.git"

# --- Platform auto-detect ---
detect_platform() {
    # ZCode (默认 ~/.agents/skills/)
    if [ -d "$HOME/.agents/skills" ] || [ -n "$ZCODE_CLI_VERSION" ]; then
        echo "$HOME/.agents/skills/session-summarize"
        return
    fi
    # CodeBuddy
    if [ -d "$HOME/.codebuddy/skills" ]; then
        echo "$HOME/.codebuddy/skills/session-summarize"
        return
    fi
    # Claude Code
    if [ -d "$HOME/.claude/skills" ] || [ -d "$HOME/.claude/plugins" ]; then
        echo "$HOME/.claude/skills/session-summarize"
        return
    fi
    # Codex (OpenAI)
    if [ -d "$HOME/.codex/skills" ] || [ -d "$HOME/.codex" ]; then
        echo "$HOME/.codex/skills/session-summarize"
        return
    fi
    # Reasonix
    if [ -d "$HOME/.reasonix/skills" ]; then
        echo "$HOME/.reasonix/skills/session-summarize"
        return
    fi
    # Fallback: generic agent-skills
    echo "$HOME/.agent-skills/session-summarize"
}

INSTALL_DIR=$(detect_platform)
LEGACY_INSTALL_DIR="$(dirname "$INSTALL_DIR")/summarize"

echo "📦 Session Summarize installer"
echo "   Target: $INSTALL_DIR"

if [ ! -d "$INSTALL_DIR" ] && [ -d "$LEGACY_INSTALL_DIR" ]; then
    echo "   Migrating legacy install: $LEGACY_INSTALL_DIR"
    mv "$LEGACY_INSTALL_DIR" "$INSTALL_DIR"
fi

if [ -d "$INSTALL_DIR" ]; then
    echo "   Already installed at $INSTALL_DIR"
    echo "🔄 Updating to latest version..."
    cd "$INSTALL_DIR"
    git pull --rebase 2>/dev/null || { cd "$HOME" && rm -rf "$INSTALL_DIR" && git clone "$REPO_SSH" "$INSTALL_DIR" 2>/dev/null || git clone "$REPO_HTTPS" "$INSTALL_DIR"; }
else
    echo "   Cloning into $INSTALL_DIR ..."
    mkdir -p "$(dirname "$INSTALL_DIR")"
    git clone "$REPO_SSH" "$INSTALL_DIR" 2>/dev/null || git clone "$REPO_HTTPS" "$INSTALL_DIR"
fi

echo ""
echo "✅ summarize skill installed!  v$(cat "$INSTALL_DIR/VERSION")"
echo "   Path:    $INSTALL_DIR"
echo "   Trigger: 总结 / session-summarize / summarize"
echo ""
echo "📊 Manage:"
echo "   Update:  cd $INSTALL_DIR && git pull"
echo "   Issues:  https://github.com/gtbwpkwjnb-alt/summarize-skill/issues"
