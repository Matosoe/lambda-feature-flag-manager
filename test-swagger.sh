#!/bin/bash

# Script para testar o Swagger UI localmente

echo "🌐 Testando Swagger UI..."
echo ""

# Health check
echo "1️⃣  Testando /health..."
docker exec feature-flag-localstack sh -c 'awslocal lambda invoke \
  --function-name feature-flag-manager \
  --payload "{\"httpMethod\":\"GET\",\"path\":\"/health\",\"headers\":{}}" \
  /tmp/health.json > /dev/null 2>&1 && cat /tmp/health.json' | \
  python3 -c "import sys, json; data=json.load(sys.stdin); print(json.dumps(json.loads(data['body']), indent=2))"

echo ""
echo "2️⃣  Testando / (Swagger UI)..."
docker exec feature-flag-localstack sh -c 'awslocal lambda invoke \
  --function-name feature-flag-manager \
  --payload "{\"httpMethod\":\"GET\",\"path\":\"/\",\"headers\":{}}" \
  /tmp/swagger.json > /dev/null 2>&1 && cat /tmp/swagger.json' | \
  python3 -c "import sys, json; data=json.load(sys.stdin); print('Status:', data['statusCode']); print('Content-Type:', data['headers']['Content-Type']); print('Body length:', len(data['body']), 'caracteres'); print('Contém Swagger UI:', 'SwaggerUIBundle' in data['body'])"

echo ""
echo "3️⃣  Testando /docs (OpenAPI Spec)..."
docker exec feature-flag-localstack sh -c 'awslocal lambda invoke \
  --function-name feature-flag-manager \
  --payload "{\"httpMethod\":\"GET\",\"path\":\"/docs\",\"headers\":{}}" \
  /tmp/docs.json > /dev/null 2>&1 && cat /tmp/docs.json' | \
  python3 -c "import sys, json; data=json.load(sys.stdin); spec=json.loads(data['body']); print('OpenAPI Version:', spec['openapi']); print('Título:', spec['info']['title']); print('Paths:', len(spec['paths']), 'endpoints')"

echo ""
echo "✅ Testes concluídos!"
echo ""
echo "📖 Para acessar o Swagger UI no browser:"
echo "   Você precisa criar um proxy HTTP que converta requisições GET"
echo "   do browser em invocações POST da Lambda."
echo ""
echo "💡 Use o seguinte comando para testar diretamente:"
echo "   ./test-swagger.sh"
