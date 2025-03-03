#!/bin/bash
set -e
echo "🚀 Building Lambda deployment package..."

# Create a temporary build directory
LAMBDA_PACKAGE="$(pwd)/app"
mkdir -p "$LAMBDA_PACKAGE"

# Save dependencies to requirements.txt
echo "📦 Saving dependencies to requirements.txt..."
uv pip freeze > requirements.txt  

# Copy application code and project configuration
echo "📋 Copying application code and project configuration..."
cp main.py requirements.txt "$LAMBDA_PACKAGE/" 

echo "✅ Build complete! Your Lambda package is ready for deployment."

