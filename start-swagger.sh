#!/bin/bash

echo "================================================"
echo "🚀 Iniciando Swagger UI para Feature Flag Manager"
echo "================================================"
echo ""

# Verificar se o LocalStack está rodando
if ! docker ps | grep -q feature-flag-localstack; then
    echo "❌ LocalStack não está rodando!"
    echo "   Execute primeiro: ./up.sh"
    exit 1
fi

# Verificar se a Lambda existe
echo "Verificando função Lambda..."
if ! docker exec feature-flag-localstack awslocal lambda list-functions 2>/dev/null | grep -q "feature-flag-manager"; then
    echo "⚠️  Função Lambda não encontrada. Criando..."
    bash run-init.sh
else
    echo "✓ Função Lambda encontrada"
fi

echo ""
echo "Iniciando proxy do Swagger UI..."
echo ""

# Iniciar o proxy em background
if command -v python3 &> /dev/null; then
    python3 swagger-proxy.py
elif command -v python &> /dev/null; then
    python swagger-proxy.py
else
    echo "❌ Python não encontrado!"
    echo "   Instale Python 3 para usar o proxy"
    exit 1
fi
