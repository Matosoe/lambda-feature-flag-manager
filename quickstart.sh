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
echo "🧾 Logs do Swagger UI: ./logs/swagger-ui.log"
echo "⏹️  Para parar: finalize o processo (PID exibido abaixo)"
echo "========================================================"
echo ""

# Iniciar proxy em background
LOG_DIR="./logs"
LOG_FILE="$LOG_DIR/swagger-ui.log"
PID_FILE="$LOG_DIR/swagger-ui.pid"
mkdir -p "$LOG_DIR"

# Encerrar proxy anterior, se existir
if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "⚠️  Encerrando Swagger UI anterior (PID: $(cat "$PID_FILE"))"
    kill "$(cat "$PID_FILE")" 2>/dev/null || true
    rm -f "$PID_FILE"
fi

if command -v python &> /dev/null; then
    PYTHONIOENCODING=UTF-8 nohup python swagger-proxy.py > "$LOG_FILE" 2>&1 &
    SWAGGER_PID=$!
    echo "$SWAGGER_PID" > "$PID_FILE"
    echo "✅ Swagger UI em segundo plano (PID: $SWAGGER_PID)"
elif command -v python3 &> /dev/null; then
    PYTHONIOENCODING=UTF-8 nohup python3 swagger-proxy.py > "$LOG_FILE" 2>&1 &
    SWAGGER_PID=$!
    echo "$SWAGGER_PID" > "$PID_FILE"
    echo "✅ Swagger UI em segundo plano (PID: $SWAGGER_PID)"
else
    echo "❌ Python não encontrado!"
    exit 1
fi
