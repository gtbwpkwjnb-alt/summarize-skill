#!/bin/bash
# summarize skill — one-line installer
# curl -sL https://raw.githubusercontent.com/gtbwpkwjnb-alt/summarize-skill/master/install.sh | bash

set -e

INSTALL_DIR="${HOME}/.agent-skills/summarize"
REPO_SSH="git@github.com:gtbwpkwjnb-alt/summarize-skill.git"
REPO_HTTPS="https://github.com/gtbwpkwjnb-alt/summarize-skill.git"

echo "📦 summarize skill installer"

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
echo "   Trigger: /总结"
echo ""
echo "📊 Manage:"
echo "   Update:  cd $INSTALL_DIR && git pull"
echo "   Issues:  https://github.com/gtbwpkwjnb-alt/summarize-skill/issues"
