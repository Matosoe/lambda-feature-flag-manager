#!/bin/bash

echo "📋 Mostrando logs do LocalStack (Ctrl+C para sair)..."
echo ""
docker-compose logs -f localstack
