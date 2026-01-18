#!/bin/bash

echo "🛑 Parando ambiente..."

# Parar containers do Docker Compose
docker-compose down

# Remover containers Lambda órfãos (criados pelo LocalStack)
echo "🧹 Limpando containers Lambda..."
docker ps -a --filter "name=feature-flag-localstack-lambda" --format "{{.ID}}" | xargs -r docker rm -f 2>/dev/null || true

# Remover network se ainda existir
echo "🧹 Limpando network..."
docker network rm lambda-feature-flag-manager_lambda-network 2>/dev/null || true

echo "✓ Ambiente parado!"
