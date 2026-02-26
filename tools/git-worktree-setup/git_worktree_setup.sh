#!/usr/bin/env bash
# git_worktree_setup.sh
# Automates the creation of a clean git worktree and runs initial setup/tests.

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <branch-name> <relative-directory-path>"
    exit 1
fi

BRANCH_NAME=$1
DIR_PATH=$2

echo "Creating git worktree '$BRANCH_NAME' at '$DIR_PATH'..."
git worktree add "$DIR_PATH" -b "$BRANCH_NAME"
if [ $? -ne 0 ]; then
    echo "Failed to create worktree."
    exit 1
fi

cd "$DIR_PATH" || exit 1

echo "Worktree created. Detecting project type for setup..."

# Auto-detect project type and run install
if [ -f "package.json" ]; then
    echo "Node.js project detected. Running npm install..."
    npm install
elif [ -f "requirements.txt" ]; then
    echo "Python project detected. Installing requirements..."
    pip install -r requirements.txt
elif [ -f "pyproject.toml" ]; then
    echo "Python Poetry project detected."
    poetry install
elif [ -f "Cargo.toml" ]; then
    echo "Rust project detected. Running cargo build..."
    cargo build
elif [ -f "go.mod" ]; then
    echo "Go project detected. Downloading modules..."
    go mod download
else
    echo "No standard package manager detected. Skipping setup step."
fi

echo "Setup complete. To verify the baseline, run your project's test command (e.g., npm test, pytest, cargo test)."
echo "Worktree ready at: $(pwd)"
