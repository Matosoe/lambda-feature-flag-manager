#!/bin/bash

# Script para parar o ambiente local

echo "🛑 Parando ambiente local..."

# Parar e remover containers
docker-compose down

echo "✅ Ambiente local parado!"
echo ""
echo "💡 Para remover os dados persistidos: rm -rf localstack-data"
