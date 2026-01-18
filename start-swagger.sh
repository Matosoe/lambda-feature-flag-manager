#!/bin/bash

echo "================================================"
echo "🚀 Iniciando Swagger UI para Feature Flag Manager"
echo "================================================"
echo ""

# Verificar se o LocalStack está rodando
if ! docker ps | grep -q feature-flag-localstack; then
    echo "❌ LocalStack não está rodando!"
    echo "   Execute primeiro: ./up.sh"
    exit 1
fi

# Verificar se a Lambda existe
echo "Verificando função Lambda..."
if ! docker exec feature-flag-localstack awslocal lambda list-functions 2>/dev/null | grep -q "feature-flag-manager"; then
    echo "⚠️  Função Lambda não encontrada. Criando..."
    bash run-init.sh
else
    echo "✓ Função Lambda encontrada"
fi

echo ""
echo "Iniciando proxy do Swagger UI em segundo plano..."
echo ""

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

# Iniciar o proxy em background
if command -v python3 &> /dev/null; then
    PYTHONIOENCODING=UTF-8 nohup python3 swagger-proxy.py > "$LOG_FILE" 2>&1 &
    SWAGGER_PID=$!
    echo "$SWAGGER_PID" > "$PID_FILE"
    echo "✅ Swagger UI em segundo plano (PID: $SWAGGER_PID)"
    echo "🧾 Logs: $LOG_FILE"
elif command -v python &> /dev/null; then
    PYTHONIOENCODING=UTF-8 nohup python swagger-proxy.py > "$LOG_FILE" 2>&1 &
    SWAGGER_PID=$!
    echo "$SWAGGER_PID" > "$PID_FILE"
    echo "✅ Swagger UI em segundo plano (PID: $SWAGGER_PID)"
    echo "🧾 Logs: $LOG_FILE"
else
    echo "❌ Python não encontrado!"
    echo "   Instale Python 3 para usar o proxy"
    exit 1
fi
