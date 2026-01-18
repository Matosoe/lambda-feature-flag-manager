#!/bin/bash

echo "📋 Mostrando logs da Lambda (Ctrl+C para sair)..."
echo ""

if command -v aws &> /dev/null; then
    aws --endpoint-url=http://localhost:4566 logs tail /aws/lambda/feature-flag-manager --follow
else
    echo "⚠️  AWS CLI não instalado. Mostrando logs do container..."
    docker-compose logs -f localstack | grep feature-flag-manager
fi
