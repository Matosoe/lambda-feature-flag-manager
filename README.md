# Feature Flag Manager API

AWS Lambda-based REST API for managing feature flags stored in AWS Systems Manager Parameter Store.

## Architecture

This project follows **SOLID principles** and clean architecture patterns:

- **Single Responsibility Principle (SRP)**: Each class has one well-defined responsibility
- **Open/Closed Principle**: Code is open for extension but closed for modification
- **Liskov Substitution Principle**: Repository interfaces can be substituted with implementations
- **Interface Segregation Principle**: Small, focused interfaces
- **Dependency Inversion Principle**: High-level modules depend on abstractions, not implementations

### Project Structure

```
├── lambda_function.py           # AWS Lambda entry point
├── src/
│   ├── handler.py              # API Gateway event handler
│   ├── router.py               # Request routing
│   ├── exceptions.py           # Custom exceptions
│   ├── controllers/
│   │   └── parameter_controller.py  # HTTP request/response handling
│   ├── services/
│   │   └── parameter_service.py     # Business logic
│   ├── repositories/
│   │   └── parameter_repository.py  # AWS Parameter Store operations
│   └── validators/
│       └── parameter_validator.py   # Input validation
├── openapi.yaml                # OpenAPI 3.0 specification
└── requirements.txt            # Python dependencies
```

## Features

### 1. List Parameters
**Endpoint**: `GET /parameters`

Lists all feature flags with `/feature-flags` prefix from Parameter Store.

**Response**:
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

### 2. Create Parameter
**Endpoint**: `POST /parameters`

Creates a new feature flag parameter.

**Request Body**:
```json
{
  "name": "my-feature",
  "value": "enabled",
  "description": "Controls my feature",
  "type": "String"
}
```

**Response** (201 Created):
```json
{
  "message": "Parameter created successfully",
  "name": "/feature-flags/my-feature"
}
```

### 3. Update Parameter
**Endpoint**: `PUT /parameters/{parameterName}`

Updates an existing feature flag parameter.

**Request Body**:
```json
{
  "value": "disabled",
  "description": "Updated description"
}
```

**Response** (200 OK):
```json
{
  "message": "Parameter updated successfully",
  "name": "/feature-flags/my-feature"
}
```

## Deployment

### Prerequisites
- AWS Account
- IAM role with SSM permissions:
  - `ssm:GetParameter`
  - `ssm:PutParameter`
  - `ssm:DescribeParameters`

### Deploy to AWS Lambda

1. Install dependencies:
```bash
pip install -r requirements.txt -t .
```

2. Create deployment package:
```bash
zip -r function.zip . -x "*.git*" "*.pyc" "__pycache__/*"
```

3. Deploy via AWS CLI:
```bash
aws lambda create-function \
  --function-name feature-flag-manager \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR-ACCOUNT:role/lambda-ssm-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip
```

4. Configure API Gateway to trigger the Lambda function

### IAM Policy Example

```json
{
  "Version": "2012-10-17",
  "Statement": [
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

## Local Development

### Testing Locally

Create a test event file `test_event.json`:
```json
{
  "httpMethod": "GET",
  "path": "/parameters",
  "body": null
}
```

Run locally:
```python
from lambda_function import lambda_handler
import json

with open('test_event.json') as f:
    event = json.load(f)

response = lambda_handler(event, None)
print(json.dumps(response, indent=2))
```

## Error Handling

The API implements comprehensive error handling:

- **400 Bad Request**: Validation errors
- **404 Not Found**: Parameter not found or invalid endpoint
- **500 Internal Server Error**: AWS service errors

All errors return JSON:
```json
{
  "error": "Error message description"
}
```

## Best Practices Implemented

1. **Separation of Concerns**: Controllers, services, repositories are clearly separated
2. **Dependency Injection**: Dependencies injected via constructors
3. **Error Handling**: Custom exceptions with proper error propagation
4. **Logging**: Structured logging throughout the application
5. **Validation**: Input validation before processing
6. **Type Hints**: Full type annotations for better IDE support
7. **Documentation**: Comprehensive docstrings following Google style

## OpenAPI Specification

The API is fully documented using OpenAPI 3.0 standard. See `openapi.yaml` for the complete specification. This enables:
- Automatic API documentation generation
- Client SDK generation
- API testing tools integration
- LLM agent integration

## License

See LICENSE file for details.
