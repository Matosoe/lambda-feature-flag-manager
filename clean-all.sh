#!/bin/bash

echo "========================================================"
echo "🧹 Limpeza Completa do Ambiente"
echo "========================================================"
echo ""
echo "⚠️  ATENÇÃO: Esta operação irá:"
echo "   • Parar todos os containers"
echo "   • Remover todos os volumes (PERDA DE DADOS)"
echo "   • Remover todas as networks"
echo "   • Remover containers Lambda órfãos"
echo ""
read -p "Deseja continuar? (s/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "Operação cancelada."
    exit 0
fi

echo ""
echo "🛑 Parando containers..."
docker-compose down -v

echo ""
echo "🧹 Removendo containers Lambda órfãos..."
docker ps -a --filter "name=feature-flag-localstack-lambda" --format "{{.ID}}" | xargs -r docker rm -f 2>/dev/null || true

echo ""
echo "🧹 Removendo network..."
docker network rm lambda-feature-flag-manager_lambda-network 2>/dev/null || true

echo ""
echo "🧹 Removendo volumes órfãos..."
docker volume prune -f

echo ""
echo "✅ Limpeza completa finalizada!"
echo ""
echo "Para reiniciar o ambiente, execute:"
echo "   bash quickstart.sh"
