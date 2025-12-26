#!/bin/bash
# Deployment script for AWS Lambda Feature Flag Manager

set -e

echo "=== Feature Flag Manager Deployment ==="

# Configuration
FUNCTION_NAME="${LAMBDA_FUNCTION_NAME:-feature-flag-manager}"
RUNTIME="python3.11"
HANDLER="lambda_function.lambda_handler"
ROLE_ARN="${LAMBDA_ROLE_ARN}"

if [ -z "$ROLE_ARN" ]; then
    echo "Error: LAMBDA_ROLE_ARN environment variable is required"
    exit 1
fi

# Clean previous build
echo "Cleaning previous build..."
rm -rf build/
rm -f function.zip

# Create build directory
echo "Creating build directory..."
mkdir -p build

# Copy source code
echo "Copying source code..."
cp -r src build/
cp lambda_function.py build/

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -t build/ --quiet

# Create deployment package
echo "Creating deployment package..."
cd build
zip -r ../function.zip . -q
cd ..

echo "Deployment package created: function.zip"
echo "Package size: $(du -h function.zip | cut -f1)"

# Deploy or update Lambda function
echo "Deploying to AWS Lambda..."

if aws lambda get-function --function-name "$FUNCTION_NAME" 2>/dev/null; then
    echo "Updating existing function..."
    aws lambda update-function-code \
        --function-name "$FUNCTION_NAME" \
        --zip-file fileb://function.zip
else
    echo "Creating new function..."
    aws lambda create-function \
        --function-name "$FUNCTION_NAME" \
        --runtime "$RUNTIME" \
        --role "$ROLE_ARN" \
        --handler "$HANDLER" \
        --zip-file fileb://function.zip \
        --timeout 30 \
        --memory-size 256
fi

echo "=== Deployment completed successfully ==="
echo "Function name: $FUNCTION_NAME"
