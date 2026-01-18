# Ambiente Local - Comandos Rápidos

## Primeiro Uso

```bash
# 1. Build
./build.sh

# 2. Subir ambiente
./up.sh

# 3. Testar
./test-api.sh
# ou
./test-python.sh
```

## Comandos Diários

```bash
./up.sh          # Subir ambiente
./down.sh        # Parar ambiente
./restart.sh     # Reiniciar
./logs.sh        # Ver logs LocalStack
./logs-lambda.sh # Ver logs da Lambda
./info.sh        # Info do ambiente
./clean.sh       # Limpar tudo
```

## Usuários Pré-configurados

- `admin@local.dev` - Admin completo
- `dev@local.dev` - Leitura + Escrita
- `analista@local.dev` - Apenas leitura

## Exemplo rápido de chamada

```bash
# Substituir URL pela URL da sua função Lambda
LAMBDA_URL="http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations"

# Listar parâmetros
curl -X GET "$LAMBDA_URL/parameters" \
  -H "X-User-Id: dev@local.dev"

# Criar parâmetro
curl -X POST "$LAMBDA_URL/parameters" \
  -H "X-User-Id: dev@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "NOVA_FEATURE",
    "value": "true",
    "type": "BOOLEAN",
    "description": "Minha nova feature",
    "lastModifiedBy": "dev@local.dev"
  }'
```

## Documentação Completa

Ver [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)
