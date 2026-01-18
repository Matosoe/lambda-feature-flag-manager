# Swagger UI - Guia Completo

## O que é?

O Swagger UI é uma interface web interativa que permite visualizar e testar a API do Feature Flag Manager diretamente do browser, sem precisar usar curl ou outras ferramentas de linha de comando.

## Como funciona?

```
┌─────────────┐     HTTP GET      ┌──────────────┐     Lambda       ┌─────────────┐
│   Browser   │ ───────────────> │ Swagger Proxy│ ──Invocation──> │  LocalStack │
│             │                   │  (Port 8080) │                  │   Lambda    │
│localhost:8080│ <─────────────── │              │ <──────────────  │             │
└─────────────┘     HTML/JSON     └──────────────┘    JSON Response └─────────────┘
```

1. **Browser** faz uma requisição HTTP normal (GET, POST, etc.)
2. **Proxy** (swagger-proxy.py) converte a requisição em um evento Lambda
3. **LocalStack** executa a função Lambda
4. **Lambda** retorna a resposta (HTML para Swagger UI, JSON para API)
5. **Proxy** retorna a resposta para o browser

## Como usar?

### 1. Certifique-se de que o ambiente está rodando

```bash
./up.sh
```

### 2. Inicie o servidor proxy do Swagger UI

```bash
./swagger-ui.sh
```

Você verá uma mensagem assim:

```
============================================================
🚀 Feature Flag Manager - Swagger UI Proxy
============================================================

✅ Servidor rodando em http://localhost:8080

📖 Acesse o Swagger UI:
   👉 http://localhost:8080/
```

### 3. Abra no browser

Acesse: **http://localhost:8080/**

## Endpoints Disponíveis

### Interface Web
- **http://localhost:8080/** - Interface completa do Swagger UI
- **http://localhost:8080/docs** - Especificação OpenAPI em JSON
- **http://localhost:8080/health** - Health check da API

### API Endpoints (testáveis pelo Swagger UI)

#### Parameters (Feature Flags)
- `GET /parameters` - Listar todos os feature flags
- `POST /parameters` - Criar novo feature flag
- `GET /parameters/{id}` - Obter feature flag específico
- `PUT /parameters/{id}` - Atualizar feature flag
- `DELETE /parameters/{id}` - Deletar feature flag

#### Users
- `GET /users` - Listar todos os usuários
- `POST /users` - Criar novo usuário (requer admin)
- `GET /users/{id}` - Obter usuário específico
- `PUT /users/{id}` - Atualizar usuário (requer admin)
- `DELETE /users/{id}` - Deletar usuário (requer admin)

## Testando a API pelo Swagger UI

### 1. Abrir um endpoint

No Swagger UI, clique em qualquer endpoint (ex: `GET /parameters`)

### 2. Clicar em "Try it out"

Isso habilita o formulário para testar o endpoint

### 3. Preencher o X-User-Id

O Swagger UI já preenche automaticamente com `dev@local.dev`, mas você pode mudar para:
- `admin@local.dev` - Acesso completo (admin)
- `dev@local.dev` - Leitura + escrita
- `analista@local.dev` - Apenas leitura

### 4. Executar

Clique em "Execute" para fazer a requisição

### 5. Ver a resposta

O Swagger UI mostra:
- Response Code (200, 403, etc.)
- Response Headers
- Response Body (JSON formatado)
- cURL command (para copiar e usar no terminal)

## Exemplos de Teste

### Listar feature flags

1. Abrir `GET /parameters`
2. Try it out
3. X-User-Id: `dev@local.dev`
4. Execute

**Resposta esperada**: Lista de todos os feature flags

### Criar feature flag

1. Abrir `POST /parameters`
2. Try it out
3. X-User-Id: `dev@local.dev`
4. Preencher o body:

```json
{
  "id": "NEW_FEATURE",
  "value": "true",
  "type": "BOOLEAN",
  "description": "Nova feature de teste",
  "lastModifiedBy": "dev@local.dev",
  "prefix": "test"
}
```

5. Execute

**Resposta esperada**: Status 201 com detalhes do parâmetro criado

### Testar permissões

Tente criar um usuário com `analista@local.dev` (sem permissão de escrita):

1. Abrir `POST /users`
2. Try it out
3. X-User-Id: `analista@local.dev`
4. Execute

**Resposta esperada**: Status 403 - Insufficient permissions

## Parar o servidor

Para parar o servidor proxy, pressione `Ctrl+C` no terminal onde ele está rodando.

## Troubleshooting

### Porta 8080 já está em uso

Se você receber erro de porta em uso, mude a porta no arquivo `swagger-proxy.py`:

```python
port = 8081  # Mudar de 8080 para 8081
```

### Lambda não responde

Verifique se o LocalStack está rodando:

```bash
docker ps | grep feature-flag-localstack
```

Se não estiver, execute:

```bash
./up.sh
```

### Erro de timeout

Aumente o timeout no `swagger-proxy.py`:

```python
result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)  # Mudar de 10 para 30
```

## Vantagens do Swagger UI

- ✅ **Visual**: Interface gráfica intuitiva
- ✅ **Interativo**: Teste direto do browser
- ✅ **Documentado**: Descrições e exemplos para cada endpoint
- ✅ **Seguro**: Valida requisições antes de enviar
- ✅ **Completo**: Mostra schemas, responses, headers
- ✅ **Exportável**: Gera código de exemplo (cURL, Python, etc.)

## Arquivos Relacionados

- `swagger-proxy.py` - Servidor HTTP que faz proxy para a Lambda
- `swagger-ui.sh` - Script para iniciar o proxy
- `src/swagger_handler.py` - Handler Lambda que serve o Swagger UI
- `openapi.yaml` - Especificação OpenAPI completa (referência)
- `test-swagger.sh` - Script de teste automatizado

## Próximos Passos

Depois de testar a API pelo Swagger UI, você pode:

1. Ver os logs da Lambda: `./logs-lambda.sh`
2. Testar via curl: `./test-api.sh`
3. Ver os logs do LocalStack: `./logs.sh`
4. Reiniciar o ambiente: `./restart.sh`
