#!/usr/bin/env bash
# install.sh — run once on a fresh Ubuntu 24.04 machine
# Installs: docker, just, pixi — then use `just <recipe>` for all r1 operations

set -euo pipefail

R1_HOME="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"

print_step() { echo -e "\n\033[1;34m▶ $1\033[0m"; }
print_ok()   { echo -e "\033[1;32m✓ $1\033[0m"; }
print_warn() { echo -e "\033[1;33m⚠ $1\033[0m"; }

# ── 1. Docker ──────────────────────────────────────────────────────────────
print_step "Checking Docker"
if ! command -v docker &>/dev/null; then
  print_step "Installing Docker"
  curl -fsSL https://get.docker.com | sh
  sudo usermod -aG docker "$USER"
  print_warn "Docker installed. You may need to log out and back in for group changes."
else
  print_ok "Docker already installed"
fi

# ── 2. NVIDIA Container Toolkit (optional) ─────────────────────────────────
print_step "Checking NVIDIA GPU"
if command -v nvidia-smi &>/dev/null; then
  if ! dpkg -l | grep -q nvidia-container-toolkit; then
    print_step "Installing NVIDIA Container Toolkit"
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
      sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
      sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker
    print_ok "NVIDIA Container Toolkit installed"
  else
    print_ok "NVIDIA Container Toolkit already installed"
  fi
else
  print_warn "No NVIDIA GPU detected — skipping NVIDIA Container Toolkit"
fi

# ── 3. just ────────────────────────────────────────────────────────────────
print_step "Checking just"
if ! command -v just &>/dev/null; then
  print_step "Installing just"
  curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to "$BIN_DIR"
  print_ok "just installed"
else
  print_ok "just already installed"
fi

# ── 4. Pixi ────────────────────────────────────────────────────────────────
print_step "Checking pixi"
if ! command -v pixi &>/dev/null; then
  print_step "Installing pixi"
  curl -fsSL https://pixi.sh/install.sh | bash
  print_ok "pixi installed"
else
  print_ok "pixi already installed"
fi

# ── 5. PATH setup — needed so `just` (installed to ~/.local/bin) is on PATH ─
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
  if [[ -f "$rc" ]] && ! grep -q '\.local/bin' "$rc"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc"
    print_ok "Added ~/.local/bin to PATH in $rc"
  fi
done

# ── 6. JUST_JUSTFILE — makes `just` work from any directory ───────────────
JUST_FILE="$(cd "$R1_HOME/.." && pwd)/justfile"
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
  if [[ -f "$rc" ]] && ! grep -q 'JUST_JUSTFILE' "$rc"; then
    echo "export JUST_JUSTFILE=\"$JUST_FILE\"" >> "$rc"
    print_ok "Set JUST_JUSTFILE in $rc"
  fi
done

# ── 7. ROS_WS_PATH ─────────────────────────────────────────────────────────
if ! grep -q 'ROS_WS_PATH' "$HOME/.bashrc" 2>/dev/null && \
   ! grep -q 'ROS_WS_PATH' "$HOME/.zshrc" 2>/dev/null; then
  print_step "Setting up ROS_WS_PATH"
  echo ""
  echo "Where is your ROS 2 workspace? (e.g. ~/workspaces/my_robot)"
  read -rp "ROS_WS_PATH: " ws_path
  ws_path="${ws_path/#\~/$HOME}"
  mkdir -p "$ws_path/src" "$ws_path/logs" "$ws_path/datasets"
  for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [[ -f "$rc" ]]; then
      echo "export ROS_WS_PATH=\"$ws_path\"" >> "$rc"
    fi
  done
  print_ok "ROS_WS_PATH=$ws_path"
fi

# ── 8. ~/.r1rc ──────────────────────────────────────────────────────────────
if [[ ! -f "$HOME/.r1rc" ]]; then
  cp "$R1_HOME/.r1rc.example" "$HOME/.r1rc"
  print_ok "Created ~/.r1rc from template — edit it for your machine"
fi

# ── 9. Tab completion for `just` ─────────────────────────────────────────
print_step "Setting up just tab completion"
# bash — just --completions requires just to be on PATH; use BIN_DIR directly
mkdir -p "$HOME/.bash_completion.d"
"$BIN_DIR/just" --completions bash > "$HOME/.bash_completion.d/just" 2>/dev/null || \
  just --completions bash > "$HOME/.bash_completion.d/just" 2>/dev/null || true
for rc in "$HOME/.bashrc"; do
  if [[ -f "$rc" ]] && ! grep -q 'bash_completion.d/just' "$rc"; then
    echo '[[ -f ~/.bash_completion.d/just ]] && source ~/.bash_completion.d/just' >> "$rc"
    print_ok "Registered just bash completion in $rc"
  fi
done
# zsh — just --completions zsh outputs a _just file; put it on fpath
mkdir -p "$HOME/.zsh/completions"
"$BIN_DIR/just" --completions zsh > "$HOME/.zsh/completions/_just" 2>/dev/null || \
  just --completions zsh > "$HOME/.zsh/completions/_just" 2>/dev/null || true
for rc in "$HOME/.zshrc"; do
  if [[ -f "$rc" ]] && ! grep -q '.zsh/completions' "$rc"; then
    echo 'fpath=(~/.zsh/completions $fpath)' >> "$rc"
    echo 'autoload -Uz compinit && compinit' >> "$rc"
    print_ok "Registered just zsh completion in $rc"
  fi
done

# ── Done ───────────────────────────────────────────────────────────────────
echo ""
print_ok "r1 installed successfully!"
echo ""
echo "  Next steps:"
echo "  1. Restart your terminal (or: source ~/.bashrc / source ~/.zshrc)"
echo "  2. Edit ~/.r1rc with your machine settings"
echo "  3. From anywhere: just pull"
echo "  4.               just start"
echo "  5.               just ws"
echo ""
echo "  All commands (run from any directory):"
echo "    just start [sim|real|isaac|isaac-lab] [pull=true]"
echo "    just stop"
echo "    just shell [\"command\"]"
echo "    just pull"
echo "    just build [tag]"
echo "    just ws"
echo ""
