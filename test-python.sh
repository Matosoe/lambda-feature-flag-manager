#!/bin/bash

echo "🐍 Executando testes Python..."
echo ""

# Verificar se Python está instalado
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python não encontrado. Por favor, instale Python 3.11+"
    exit 1
fi

# Verificar se requests está instalado
PYTHON_CMD=$(command -v python3 || command -v python)

$PYTHON_CMD -c "import requests" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Instalando dependências..."
    pip install -r requirements-dev.txt
    echo ""
fi

# Executar testes
$PYTHON_CMD test_local_environment.py
