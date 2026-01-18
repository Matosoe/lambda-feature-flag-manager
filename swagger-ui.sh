#!/bin/bash

# Script para iniciar o servidor proxy do Swagger UI

echo "🚀 Iniciando servidor proxy do Swagger UI..."
echo ""

# Verificar se o LocalStack está rodando
if ! docker ps | grep -q feature-flag-localstack; then
    echo "❌ LocalStack não está rodando!"
    echo "   Execute primeiro: ./up.sh"
    exit 1
fi

# Verificar se a Lambda existe
if ! docker exec feature-flag-localstack awslocal lambda list-functions 2>/dev/null | grep -q "feature-flag-manager"; then
    echo "❌ Função Lambda não encontrada!"
    echo "   Execute: ./restart.sh"
    exit 1
fi

# Verificar se Python 3 está disponível
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "   Instale Python 3 para usar o proxy"
    exit 1
fi

# Iniciar o proxy
python3 swagger-proxy.py
