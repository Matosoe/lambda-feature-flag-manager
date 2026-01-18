#!/bin/bash

echo "🧹 Limpando ambiente..."
echo ""
echo "⚠️  ATENÇÃO: Isso vai remover:"
echo "  - Todos os containers"
echo "  - Todos os volumes"
echo "  - Todos os dados em localstack-data/"
echo ""
read -p "Tem certeza? (s/N) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "Removendo containers e volumes..."
    docker-compose down -v
    
    echo "Removendo dados locais..."
    rm -rf localstack-data
    
    echo ""
    echo "✓ Limpeza concluída!"
else
    echo "Operação cancelada."
fi
