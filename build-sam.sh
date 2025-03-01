#!/bin/bash
set -e
echo "🚀 Building Lambda deployment package..."

# Create a temporary build directory
BUILD_DIR="$(pwd)/.aws-sam/build/GenAIFunction"
mkdir -p "$BUILD_DIR"

# Copy application code and project configuration
echo "📋 Copying application code and project configuration..."
cp main.py requirements.txt .env "$BUILD_DIR/" 
# Move to build directory
cd "$BUILD_DIR"

# Install dependencies from requirements.txt
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt --target ./

# Clean up unnecessary files
echo "🧹 Cleaning up package..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete

# Flatten the dependencies to ensure everything is packaged correctly for Lambda
echo "📦 Flattening dependencies..."
cp -r ./* .  # Copy the dependencies to the build directory

# Remove unnecessary files after installation
rm -rf ./*.dist-info
rm -rf ./*.egg-info
rm -rf ./bin ./lib  # Remove unnecessary directories from the virtual environment

echo "✅ Build complete! Your Lambda package is ready for deployment."Ste
echo "You can now run 'sam deploy --guided' to deploy the application."
