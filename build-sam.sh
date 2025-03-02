#!/bin/bash
set -e
echo "🚀 Building Lambda deployment package..."

# Create a temporary build directory
BUILD_DIR="$(pwd)/.aws-sam/build/GenAIFunction"
mkdir -p "$BUILD_DIR"

# Save dependencies to requirements.txt
echo "📦 Saving dependencies to requirements.txt..."
uv pip freeze > requirements.txt  

# Copy application code and project configuration
echo "📋 Copying application code and project configuration..."
cp main.py requirements.txt "$BUILD_DIR/" 

# Move to build directory
cd "$BUILD_DIR"

# Use a virtual environment to install dependencies
echo "📦 Setting up virtual environment..."
uv venv .venv
source .venv/bin/activate

# Install dependencies from requirements.txt
echo "📦 Installing dependencies from requirements.txt..."
uv pip install --no-cache-dir -r requirements.txt --target ./

# Clean up unnecessary files
echo "🧹 Cleaning up package..."
rm -rf **/*.pyc  # Remove Python bytecode files
rm -rf **/__pycache__  # Remove __pycache__ directories
rm -rf ./*.dist-info
rm -rf ./*.egg-info
rm -rf ./bin ./lib  # Remove unnecessary directories from the virtual environment

# Flatten the dependencies (avoid copying the same files multiple times)
echo "📦 Flattening dependencies..."
for dir in $(find . -type d); do
  cp -r $dir/* . 2>/dev/null || true  # Avoid errors if files already exist
done

echo "✅ Build complete! Your Lambda package is ready for deployment."

