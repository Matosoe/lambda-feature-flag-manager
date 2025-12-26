# Quick Start Guide - Feature Flag Manager API

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install development dependencies (for testing)
pip install -r requirements-dev.txt
```

## Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_validator.py

# Run with verbose output
pytest -v
```

## Local Testing

Use the provided test event files to test locally:

```python
import json
from lambda_function import lambda_handler

# Test listing parameters
with open('test_event_list.json') as f:
    event = json.load(f)
response = lambda_handler(event, None)
print(json.dumps(response, indent=2))

# Test creating parameter
with open('test_event_create.json') as f:
    event = json.load(f)
response = lambda_handler(event, None)
print(json.dumps(response, indent=2))

# Test updating parameter
with open('test_event_update.json') as f:
    event = json.load(f)
response = lambda_handler(event, None)
print(json.dumps(response, indent=2))
```

## Deployment

### Windows
```powershell
# Set environment variables
$env:LAMBDA_ROLE_ARN = "arn:aws:iam::YOUR-ACCOUNT:role/lambda-ssm-role"
$env:LAMBDA_FUNCTION_NAME = "feature-flag-manager"

# Deploy
.\deploy.ps1
```

### Linux/Mac
```bash
# Set environment variables
export LAMBDA_ROLE_ARN="arn:aws:iam::YOUR-ACCOUNT:role/lambda-ssm-role"
export LAMBDA_FUNCTION_NAME="feature-flag-manager"

# Make script executable
chmod +x deploy.sh

# Deploy
./deploy.sh
```

## API Usage Examples

### List All Feature Flags

**Request:**
```http
GET /parameters HTTP/1.1
Content-Type: application/json
```

**Response:**
```json
{
  "parameters": [
    {
      "name": "my-feature",
      "full_name": "/feature-flags/my-feature",
      "type": "String",
      "value": "enabled",
      "description": "Controls my feature",
      "last_modified": "2025-12-25T20:00:00+00:00"
    }
  ]
}
```

### Create Feature Flag

**Request:**
```http
POST /parameters HTTP/1.1
Content-Type: application/json

{
  "name": "new-feature",
  "value": "enabled",
  "description": "New feature flag",
  "type": "String"
}
```

**Response:**
```json
{
  "message": "Parameter created successfully",
  "name": "/feature-flags/new-feature"
}
```

### Update Feature Flag

**Request:**
```http
PUT /parameters/my-feature HTTP/1.1
Content-Type: application/json

{
  "value": "disabled",
  "description": "Updated description"
}
```

**Response:**
```json
{
  "message": "Parameter updated successfully",
  "name": "/feature-flags/my-feature"
}
```

## Using with curl

```bash
# List parameters
curl -X GET https://your-api-gateway-url/prod/parameters

# Create parameter
curl -X POST https://your-api-gateway-url/prod/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-feature",
    "value": "enabled",
    "description": "Test feature"
  }'

# Update parameter
curl -X PUT https://your-api-gateway-url/prod/parameters/test-feature \
  -H "Content-Type: application/json" \
  -d '{
    "value": "disabled"
  }'
```

## Using with Python (boto3)

```python
import boto3
import json

lambda_client = boto3.client('lambda')

# Invoke Lambda directly
response = lambda_client.invoke(
    FunctionName='feature-flag-manager',
    InvocationType='RequestResponse',
    Payload=json.dumps({
        'httpMethod': 'GET',
        'path': '/parameters'
    })
)

result = json.loads(response['Payload'].read())
print(json.dumps(result, indent=2))
```

## Using with LLM Agents

The API is designed to be LLM-agent friendly:

1. **OpenAPI Specification**: Use `openapi.yaml` to configure your LLM agent
2. **Clear Error Messages**: All errors include descriptive messages
3. **Consistent Response Format**: All responses follow the same JSON structure
4. **RESTful Design**: Standard HTTP methods and status codes

### Example LLM Agent Configuration

```yaml
tools:
  - name: list_feature_flags
    endpoint: GET /parameters
    description: Lists all feature flags
    
  - name: create_feature_flag
    endpoint: POST /parameters
    description: Creates a new feature flag
    parameters:
      - name: name (required)
      - value: value (required)
      - description: description (optional)
      - type: type (optional, default: String)
    
  - name: update_feature_flag
    endpoint: PUT /parameters/{name}
    description: Updates an existing feature flag
    parameters:
      - value: new value (optional)
      - description: new description (optional)
```

## IAM Setup

Create an IAM role for Lambda with this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter",
        "ssm:PutParameter",
        "ssm:DescribeParameters"
      ],
      "Resource": "arn:aws:ssm:*:*:parameter/feature-flags/*"
    }
  ]
}
```

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure Lambda role has SSM permissions
2. **Parameter Not Found**: Check parameter name doesn't include `/feature-flags/` prefix
3. **Validation Error**: Check request body format matches OpenAPI spec
4. **Deployment Failed**: Verify AWS CLI is configured and LAMBDA_ROLE_ARN is set

### Enable Debug Logging

Set Lambda environment variable:
```
LOG_LEVEL=DEBUG
```

## Next Steps

1. Configure API Gateway to trigger the Lambda function
2. Set up CloudWatch alarms for monitoring
3. Add custom domain name (optional)
4. Configure CORS if needed for web clients
5. Set up CI/CD pipeline for automated deployments

## Support

- Check `README.md` for detailed documentation
- Review `IMPLEMENTATION_PLAN.md` for architecture details
- Consult `openapi.yaml` for complete API specification
