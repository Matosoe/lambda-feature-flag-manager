#!/bin/bash

echo "🧪 Testando API..."
echo ""

FUNCTION_URL="http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations"

# Verificar se curl está disponível
if ! command -v curl &> /dev/null; then
    echo "❌ curl não encontrado. Por favor, instale curl."
    exit 1
fi

echo "1. Listando parâmetros..."
curl -s -X GET "$FUNCTION_URL/parameters" -H "X-User-Id: dev@local.dev" | python -m json.tool 2>/dev/null || curl -s -X GET "$FUNCTION_URL/parameters" -H "X-User-Id: dev@local.dev"
echo ""
echo ""

echo "2. Obtendo parâmetro específico (DARK_MODE)..."
curl -s -X GET "$FUNCTION_URL/parameters/DARK_MODE" -H "X-User-Id: dev@local.dev" | python -m json.tool 2>/dev/null || curl -s -X GET "$FUNCTION_URL/parameters/DARK_MODE" -H "X-User-Id: dev@local.dev"
echo ""
echo ""

echo "3. Listando usuários..."
curl -s -X GET "$FUNCTION_URL/users" -H "X-User-Id: admin@local.dev" | python -m json.tool 2>/dev/null || curl -s -X GET "$FUNCTION_URL/users" -H "X-User-Id: admin@local.dev"
echo ""
echo ""

echo "✓ Testes concluídos!"
