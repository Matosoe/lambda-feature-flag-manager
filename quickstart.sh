#!/bin/bash

echo "========================================================"
echo "🚀 Feature Flag Manager - Inicialização Completa"
echo "========================================================"
echo ""

# 1. Verificar se o LocalStack está rodando
echo "1️⃣  Verificando LocalStack..."
if docker ps --filter "name=feature-flag-localstack" --filter "status=running" | grep -q feature-flag-localstack; then
    echo "   ✓ LocalStack já está rodando"
else
    echo "   ⚠️  LocalStack não está rodando. Iniciando..."
    ./up.sh
    echo ""
    echo "   ⏳ Aguardando LocalStack inicializar (10s)..."
    sleep 10
fi

echo ""

# 2. Inicializar Lambda e usuários
echo "2️⃣  Inicializando Lambda e usuários..."
bash run-init.sh

echo ""

# 3. Iniciar proxy do Swagger
echo "3️⃣  Iniciando Swagger UI Proxy..."
echo ""
echo "========================================================"
echo "✅ Ambiente inicializado com sucesso!"
echo "========================================================"
echo ""
echo "📖 Swagger UI: http://localhost:8080"
echo ""
echo "👥 Usuários disponíveis:"
echo "   • admin@local.dev     - Admin (todas permissões)"
echo "   • dev@local.dev       - Desenvolvedor (leitura + escrita)"
echo "   • analista@local.dev  - Analista (apenas leitura)"
echo ""
echo "⏹️  Pressione Ctrl+C para parar o servidor"
echo "========================================================"
echo ""

# Iniciar proxy
if command -v python &> /dev/null; then
    python swagger-proxy.py
elif command -v python3 &> /dev/null; then
    python3 swagger-proxy.py
else
    echo "❌ Python não encontrado!"
    exit 1
fi
