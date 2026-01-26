#!/bin/bash
set -e
cd "$(dirname "$0")"
# Exemplo: zip -r lambda.zip lambda_function.py requirements.txt swagger/
# Exemplo: aws lambda update-function-code --function-name <nome> --zip-file fileb://lambda.zip
# Exemplo: aws s3 sync swagger/swagger-ui/ s3://<bucket-name>/swagger-ui/
# Configure o bucket e credenciais AWS antes de rodar
