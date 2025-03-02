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
python -m venv venv
source venv/bin/activate

# Install dependencies from requirements.txt
echo "📦 Installing dependencies from requirements.txt..."
pip install --no-cache-dir -r requirements.txt --target ./

# Clean up unnecessary files
echo "🧹 Cleaning up package..."
find . -name "*.pyc" -exec rm -f {} \;
find . -name "__pycache__" -exec rm -rf {} \;
find . -name "*.dist-info" -exec rm -rf {} \;


# Flatten the dependencies (avoid copying the same files multiple times)
echo "📦 Flattening dependencies..."
for dir in $(find . -type d); do
  cp -r $dir/* . 2>/dev/null || true  # Avoid errors if files already exist
done

# Remove unnecessary files after installation
rm -rf ./*.dist-info
rm -rf ./*.egg-info
rm -rf ./bin ./lib  # Remove unnecessary directories from the virtual environment

echo "✅ Build complete! Your Lambda package is ready for deployment."Ste
echo "You can now run 'sam deploy --guided' to deploy the application."
