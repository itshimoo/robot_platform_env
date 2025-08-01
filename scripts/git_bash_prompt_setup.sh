#!/bin/bash

# Git prompt script destination
GIT_PROMPT=~/.git-prompt.sh

echo "🔧 Setting up Git-enhanced Bash prompt..."

# Step 1: Download git-prompt.sh if not already present
if [ ! -f "$GIT_PROMPT" ]; then
  echo "📥 Downloading git-prompt.sh..."
  curl -fsSL https://raw.githubusercontent.com/git/git/master/contrib/completion/git-prompt.sh -o "$GIT_PROMPT"
else
  echo "✅ git-prompt.sh already exists."
fi

# Step 2: Append to .bashrc if not already set
if ! grep -q "git-prompt.sh" ~/.bashrc; then
  echo "✍️ Updating ~/.bashrc..."

  cat << 'EOF' >> ~/.bashrc

# === Git-aware colored prompt ===
if [ -f ~/.git-prompt.sh ]; then
  source ~/.git-prompt.sh
fi

export GIT_PS1_SHOWDIRTYSTATE=1
export GIT_PS1_SHOWUNTRACKEDFILES=1
export GIT_PS1_SHOWSTASHSTATE=1

# Colored Bash prompt with Git branch/status
export PS1='\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\[\033[01;33m\]$(__git_ps1 " (%s)")\[\033[00m\]\$ '
# === End Git prompt block ===
EOF

  echo "✅ .bashrc updated."
else
  echo "⚠️ Git prompt already configured in .bashrc. Skipping changes."
fi

echo "✅ Done. Run 'source ~/.bashrc' or restart terminal to activate."
