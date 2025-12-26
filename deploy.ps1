# Deployment script for AWS Lambda Feature Flag Manager (Windows)

$ErrorActionPreference = "Stop"

Write-Host "=== Feature Flag Manager Deployment ===" -ForegroundColor Green

# Configuration
$FUNCTION_NAME = if ($env:LAMBDA_FUNCTION_NAME) { $env:LAMBDA_FUNCTION_NAME } else { "feature-flag-manager" }
$RUNTIME = "python3.11"
$HANDLER = "lambda_function.lambda_handler"
$ROLE_ARN = $env:LAMBDA_ROLE_ARN

if (-not $ROLE_ARN) {
    Write-Host "Error: LAMBDA_ROLE_ARN environment variable is required" -ForegroundColor Red
    exit 1
}

# Clean previous build
Write-Host "Cleaning previous build..." -ForegroundColor Yellow
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "function.zip") { Remove-Item -Force "function.zip" }

# Create build directory
Write-Host "Creating build directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path "build" -Force | Out-Null

# Copy source code
Write-Host "Copying source code..." -ForegroundColor Yellow
Copy-Item -Recurse "src" "build\"
Copy-Item "lambda_function.py" "build\"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt -t build\ --quiet

# Create deployment package
Write-Host "Creating deployment package..." -ForegroundColor Yellow
Compress-Archive -Path "build\*" -DestinationPath "function.zip" -Force

$zipSize = (Get-Item "function.zip").Length / 1MB
Write-Host "Deployment package created: function.zip" -ForegroundColor Green
Write-Host ("Package size: {0:N2} MB" -f $zipSize) -ForegroundColor Green

# Deploy or update Lambda function
Write-Host "Deploying to AWS Lambda..." -ForegroundColor Yellow

try {
    aws lambda get-function --function-name $FUNCTION_NAME 2>$null
    Write-Host "Updating existing function..." -ForegroundColor Yellow
    aws lambda update-function-code `
        --function-name $FUNCTION_NAME `
        --zip-file fileb://function.zip
} catch {
    Write-Host "Creating new function..." -ForegroundColor Yellow
    aws lambda create-function `
        --function-name $FUNCTION_NAME `
        --runtime $RUNTIME `
        --role $ROLE_ARN `
        --handler $HANDLER `
        --zip-file fileb://function.zip `
        --timeout 30 `
        --memory-size 256
}

Write-Host "=== Deployment completed successfully ===" -ForegroundColor Green
Write-Host "Function name: $FUNCTION_NAME" -ForegroundColor Green
