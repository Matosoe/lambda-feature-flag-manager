#!/bin/bash

echo "==================================="
echo "Inicializando Feature Flag Manager"
echo "==================================="

# Aguardar LocalStack estar pronto
sleep 2

# Criar pacote ZIP da Lambda
echo "Criando pacote ZIP da Lambda..."
cd /tmp
mkdir -p lambda-package
cd lambda-package

# Copiar código fonte
cp -r /docker-entrypoint-initaws.d/src ./
cp /docker-entrypoint-initaws.d/lambda_function.py ./

# Instalar dependências
pip3 install -q --target . boto3 botocore PyYAML

# Criar ZIP
zip -q -r /tmp/function.zip .
cd /tmp
rm -rf lambda-package

# Criar função Lambda
echo "Criando função Lambda..."
awslocal lambda create-function \
    --function-name feature-flag-manager \
    --runtime python3.11 \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --handler lambda_function.lambda_handler \
    --timeout 30 \
    --memory-size 512 \
    --zip-file fileb:///tmp/function.zip

# Criar URL de função Lambda (simula API Gateway)
echo "Criando Function URL..."
awslocal lambda create-function-url-config \
    --function-name feature-flag-manager \
    --auth-type NONE

# Obter a URL da função
FUNCTION_URL=$(awslocal lambda get-function-url-config \
    --function-name feature-flag-manager \
    --query 'FunctionUrl' \
    --output text)

# Criar estrutura inicial de usuários no Parameter Store
echo "Criando estrutura inicial de usuários..."
awslocal ssm put-parameter \
    --name "/feature-flags/users" \
    --value '{
  "usuarios": [
    {
      "id": "admin@local.dev",
      "nome": "Admin Local",
      "permissoes": {
        "leitura": true,
        "escrita": true,
        "admin": true
      },
      "ativo": true
    },
    {
      "id": "dev@local.dev",
      "nome": "Desenvolvedor",
      "permissoes": {
        "leitura": true,
        "escrita": true,
        "admin": false
      },
      "ativo": true
    },
    {
      "id": "analista@local.dev",
      "nome": "Analista",
      "permissoes": {
        "leitura": true,
        "escrita": false,
        "admin": false
      },
      "ativo": true
    }
  ]
}' \
    --type String \
    --description "Feature flags users with permissions" \
    --overwrite

# Criar alguns parâmetros de exemplo
echo "Criando feature flags de exemplo..."

# Flag UI - Dark Mode
awslocal ssm put-parameter \
    --name "/feature-flags/flags/ui/DARK_MODE" \
    --value '{
  "id": "DARK_MODE",
  "value": "true",
  "type": "BOOLEAN",
  "description": "Habilita modo escuro na interface",
  "lastModifiedAt": "2026-01-14T10:00:00Z",
  "lastModifiedBy": "admin@local.dev",
  "previousVersion": null
}' \
    --type String \
    --description "UI - Dark mode toggle" \
    --overwrite

# Flag API - Max Retry
awslocal ssm put-parameter \
    --name "/feature-flags/flags/api/MAX_RETRY" \
    --value '{
  "id": "MAX_RETRY",
  "value": "3",
  "type": "INTEGER",
  "description": "Número máximo de tentativas de retry nas chamadas de API",
  "lastModifiedAt": "2026-01-14T10:00:00Z",
  "lastModifiedBy": "dev@local.dev",
  "previousVersion": null
}' \
    --type String \
    --description "API - Max retry attempts" \
    --overwrite

# Flag global - Maintenance Mode
awslocal ssm put-parameter \
    --name "/feature-flags/flags/MAINTENANCE_MODE" \
    --value '{
  "id": "MAINTENANCE_MODE",
  "value": "false",
  "type": "BOOLEAN",
  "description": "Ativa modo de manutenção global",
  "lastModifiedAt": "2026-01-14T10:00:00Z",
  "lastModifiedBy": "admin@local.dev",
  "previousVersion": null
}' \
    --type String \
    --description "Global - Maintenance mode" \
    --overwrite

# Flag de configuração - Timeout
awslocal ssm put-parameter \
    --name "/feature-flags/flags/config/API_TIMEOUT" \
    --value '{
  "id": "API_TIMEOUT",
  "value": "30.5",
  "type": "DOUBLE",
  "description": "Timeout padrão para chamadas de API (em segundos)",
  "lastModifiedAt": "2026-01-14T10:00:00Z",
  "lastModifiedBy": "dev@local.dev",
  "previousVersion": null
}' \
    --type String \
    --description "Config - API timeout" \
    --overwrite

echo ""
echo "==================================="
echo "✓ Inicialização concluída!"
echo "==================================="
echo ""
echo "📍 Lambda Function URL: $FUNCTION_URL"
echo ""
echo "👥 Usuários disponíveis:"
echo "  - admin@local.dev (Admin - todas permissões)"
echo "  - dev@local.dev (Desenvolvedor - leitura e escrita)"
echo "  - analista@local.dev (Analista - apenas leitura)"
echo ""
echo "🚩 Feature flags criadas:"
echo "  - /feature-flags/flags/ui/DARK_MODE"
echo "  - /feature-flags/flags/api/MAX_RETRY"
echo "  - /feature-flags/flags/config/API_TIMEOUT"
echo "  - /feature-flags/flags/MAINTENANCE_MODE"
echo ""
echo "📖 Exemplos de uso:"
echo ""
echo "# Listar todos os parâmetros"
echo "curl -X GET $FUNCTION_URL/parameters \\"
echo "  -H 'X-User-Id: dev@local.dev'"
echo ""
echo "# Obter parâmetro específico"
echo "curl -X GET $FUNCTION_URL/parameters/DARK_MODE \\"
echo "  -H 'X-User-Id: dev@local.dev'"
echo ""
echo "# Criar novo parâmetro"
echo "curl -X POST $FUNCTION_URL/parameters \\"
echo "  -H 'X-User-Id: dev@local.dev' \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"id\": \"NEW_FEATURE\", \"value\": \"true\", \"type\": \"BOOLEAN\", \"description\": \"Nova feature\", \"lastModifiedBy\": \"dev@local.dev\"}'"
echo ""
echo "# Listar usuários"
echo "curl -X GET $FUNCTION_URL/users \\"
echo "  -H 'X-User-Id: admin@local.dev'"
echo ""
echo "==================================="
