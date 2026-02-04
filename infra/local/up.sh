#!/bin/bash

# Script para subir o ambiente local com LocalStack

echo "🚀 Iniciando ambiente local..."

# Criar diretório de dados se não existir
mkdir -p localstack-data

# Subir containers
docker-compose up -d

# Aguardar LocalStack estar pronto
echo "⏳ Aguardando LocalStack inicializar..."
sleep 10

# Verificar se LocalStack está rodando
if docker ps | grep -q lambda-feature-flag-localstack; then
    echo "✅ LocalStack está rodando!"
    echo ""
    echo "📋 Serviços disponíveis:"
    echo "   - LocalStack Gateway: http://localhost:4566"
    echo ""
    echo "💡 Para verificar logs: docker-compose logs -f"
    echo "💡 Para parar: ./down.sh"
else
    echo "❌ Erro ao iniciar LocalStack"
    exit 1
fi
