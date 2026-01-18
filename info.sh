#!/bin/bash

echo "==================================="
echo "Feature Flag Manager - Ambiente Local"
echo "==================================="
echo ""
echo "📍 Endpoint LocalStack: http://localhost:4566"
echo ""

# Tentar obter Function URL
if command -v aws &> /dev/null; then
    FUNCTION_URL=$(aws --endpoint-url=http://localhost:4566 lambda get-function-url-config \
        --function-name feature-flag-manager \
        --query 'FunctionUrl' \
        --output text 2>/dev/null)
    
    if [ -n "$FUNCTION_URL" ]; then
        echo "📍 Lambda Function URL: $FUNCTION_URL"
    else
        echo "⚠️  Lambda Function URL ainda não disponível"
    fi
else
    echo "📍 Lambda Function URL: http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations"
fi

echo ""
echo "👥 Usuários disponíveis:"
echo "  - admin@local.dev (todas permissões)"
echo "  - dev@local.dev (leitura + escrita)"
echo "  - analista@local.dev (apenas leitura)"
echo ""
echo "📚 Comandos úteis:"
echo "  ./test-api.sh     - Testa a API"
echo "  ./test-python.sh  - Testa a API (Python)"
echo "  ./logs.sh         - Ver logs do LocalStack"
echo "  ./logs-lambda.sh  - Ver logs da Lambda"
echo ""
echo "==================================="
