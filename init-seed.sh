#!/bin/bash

# Script único para cadastrar dados iniciais (usuários e parâmetros)

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

echo "✓ Usuários criados com sucesso!"

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

# Flags de contingência
awslocal ssm put-parameter \
    --name "/feature-flags/flags/contingencia/CONTINGENCIA_TOTAL" \
    --value '{
  "id": "CONTINGENCIA_TOTAL",
  "value": "true",
  "type": "BOOLEAN",
  "description": "Habilita a contingência total, online e batch, em todos os leiautes",
  "lastModifiedAt": "2026-01-18T10:00:00Z",
  "lastModifiedBy": "admin@local.dev",
  "previousVersion": null
}' \
    --type String \
    --description "Habilita a contingência total, online e batch, em todos os leiautes" \
    --overwrite

awslocal ssm put-parameter \
    --name "/feature-flags/flags/contingencia/CONTINGENCIA_TOTAL_ONLINE" \
    --value '{
  "id": "CONTINGENCIA_TOTAL_ONLINE",
  "value": "true",
  "type": "BOOLEAN",
  "description": "Habilita a contingência total, apenas no online, em todos os leiautes",
  "lastModifiedAt": "2026-01-18T10:00:00Z",
  "lastModifiedBy": "admin@local.dev",
  "previousVersion": null
}' \
    --type String \
    --description "Habilita a contingência total, apenas no online, em todos os leiautes" \
    --overwrite

awslocal ssm put-parameter \
    --name "/feature-flags/flags/contingencia/CONTINGENCIA_TOTAL_BATCH" \
    --value '{
  "id": "CONTINGENCIA_TOTAL_BATCH",
  "value": "true",
  "type": "BOOLEAN",
  "description": "Habilita a contingência total, apenas no batch, em todos os leiautes",
  "lastModifiedAt": "2026-01-18T10:00:00Z",
  "lastModifiedBy": "admin@local.dev",
  "previousVersion": null
}' \
    --type String \
    --description "Habilita a contingência total, apenas no batch, em todos os leiautes" \
    --overwrite

awslocal ssm put-parameter \
    --name "/feature-flags/flags/contingencia/CONTINGENCIA_DDA0110" \
    --value '{
  "id": "CONTINGENCIA_DDA0110",
  "value": "true",
  "type": "BOOLEAN",
  "description": "Habilita a contingência da mensagem de consulta de boletos no mercado, DDA0110",
  "lastModifiedAt": "2026-01-18T10:00:00Z",
  "lastModifiedBy": "admin@local.dev",
  "previousVersion": null
}' \
    --type String \
    --description "Habilita a contingência da mensagem de consulta de boletos no mercado, DDA0110" \
    --overwrite

echo "✓ Parâmetros criados com sucesso!"
