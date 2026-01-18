#!/bin/bash

echo "🚀 Subindo ambiente LocalStack + Lambda..."
echo ""

# Tornar o script de inicialização executável
chmod +x init-localstack.sh

# Subir containers
docker-compose up -d

echo ""
echo "⏳ Aguardando LocalStack inicializar (30 segundos)..."
sleep 30

echo ""
echo "✓ Ambiente pronto!"
echo ""

# Mostrar informações
./info.sh
