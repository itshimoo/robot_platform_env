#!/bin/bash

# Enable Docker BuildKit for faster builds
echo "🚀 Enabling Docker BuildKit for faster builds..."

# Add BuildKit environment variable to shell profile
if [[ "$SHELL" == *"bash"* ]]; then
    if ! grep -q "DOCKER_BUILDKIT=1" ~/.bashrc; then
        echo "" >> ~/.bashrc
        echo "# Enable Docker BuildKit for faster builds" >> ~/.bashrc
        echo "export DOCKER_BUILDKIT=1" >> ~/.bashrc
        echo "✅ Added BuildKit to ~/.bashrc"
    else
        echo "✅ BuildKit already enabled in ~/.bashrc"
    fi
elif [[ "$SHELL" == *"zsh"* ]]; then
    if ! grep -q "DOCKER_BUILDKIT=1" ~/.zshrc; then
        echo "" >> ~/.zshrc
        echo "# Enable Docker BuildKit for faster builds" >> ~/.zshrc
        echo "export DOCKER_BUILDKIT=1" >> ~/.zshrc
        echo "✅ Added BuildKit to ~/.zshrc"
    else
        echo "✅ BuildKit already enabled in ~/.zshrc"
    fi
else
    echo "⚠️  Unknown shell: $SHELL"
    echo "Please manually add 'export DOCKER_BUILDKIT=1' to your shell profile"
fi

# Enable BuildKit for current session
export DOCKER_BUILDKIT=1

echo "🎉 BuildKit enabled! Your Docker builds will now be faster."
echo "💡 Restart your terminal or run 'source ~/.bashrc' to apply changes." 