#!/bin/bash

# Script de demonstração do Swagger UI

echo "════════════════════════════════════════════════════════════════"
echo "         Feature Flag Manager - Swagger UI Demo"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Verificar se o ambiente está rodando
if ! docker ps | grep -q feature-flag-localstack; then
    echo "⚠️  Ambiente não está rodando. Subindo agora..."
    ./up.sh
    echo ""
fi

echo "📋 Informações do Sistema:"
echo "  • LocalStack: http://localhost:4566"
echo "  • Lambda Function: feature-flag-manager"
echo "  • Swagger UI: http://localhost:8080"
echo ""

echo "👥 Usuários disponíveis:"
echo "  • admin@local.dev     (Admin - todas permissões)"
echo "  • dev@local.dev       (Dev - leitura + escrita)"
echo "  • analista@local.dev  (Analista - apenas leitura)"
echo ""

echo "🚀 Testando Lambda..."
docker exec feature-flag-localstack sh -c 'awslocal lambda invoke \
  --function-name feature-flag-manager \
  --payload "{\"httpMethod\":\"GET\",\"path\":\"/health\",\"headers\":{}}" \
  /tmp/demo_health.json > /dev/null 2>&1 && cat /tmp/demo_health.json' | \
  python3 -c "import sys, json; data=json.load(sys.stdin); print('  ✓ Lambda Status:', 'OK' if data['statusCode'] == 200 else 'ERRO')"

echo ""
echo "📊 OpenAPI Specification:"
docker exec feature-flag-localstack sh -c 'awslocal lambda invoke \
  --function-name feature-flag-manager \
  --payload "{\"httpMethod\":\"GET\",\"path\":\"/docs\",\"headers\":{}}" \
  /tmp/demo_docs.json > /dev/null 2>&1 && cat /tmp/demo_docs.json' | \
  python3 -c "import sys, json; data=json.load(sys.stdin); spec=json.loads(data['body']); print('  • Versão:', spec['openapi']); print('  • Título:', spec['info']['title']); print('  • Endpoints:', len(spec['paths']))"

echo ""
echo "🌐 Swagger UI HTML:"
docker exec feature-flag-localstack sh -c 'awslocal lambda invoke \
  --function-name feature-flag-manager \
  --payload "{\"httpMethod\":\"GET\",\"path\":\"/\",\"headers\":{}}" \
  /tmp/demo_swagger.json > /dev/null 2>&1 && cat /tmp/demo_swagger.json' | \
  python3 -c "import sys, json; data=json.load(sys.stdin); print('  • Status:', data['statusCode']); print('  • Content-Type:', data['headers']['Content-Type']); print('  • Tamanho:', len(data['body']), 'chars'); print('  • Contém SwaggerUI:', 'SwaggerUIBundle' in data['body'])"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🎯 Para acessar o Swagger UI no browser:"
echo ""
echo "   1. Execute em outro terminal:"
echo "      ./swagger-ui.sh"
echo ""
echo "   2. Abra no browser:"
echo "      http://localhost:8080/"
echo ""
echo "   3. Teste os endpoints interativamente!"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📚 Documentação:"
echo "   • ./help.sh            - Lista todos os comandos"
echo "   • cat SWAGGER_GUIDE.md - Guia completo do Swagger UI"
echo "   • cat SWAGGER_README.md - Resumo da implementação"
echo ""
echo "✨ Tudo pronto para uso!"
echo ""
