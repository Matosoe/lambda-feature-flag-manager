# Gerenciamento de Usuários e Permissões

## 📋 Visão Geral

O sistema de feature flags agora inclui gerenciamento completo de usuários com controle de permissões baseado em roles. Todos os usuários são armazenados em um único parâmetro no AWS Parameter Store.

## 🔐 Sistema de Permissões

### Tipos de Permissão

1. **leitura** (read): Permite visualizar parâmetros
   - Listar todos os parâmetros
   - Ver detalhes de um parâmetro específico
   - Listar usuários

2. **escrita** (write): Permite modificar parâmetros
   - Criar novos parâmetros
   - Atualizar parâmetros existentes
   - Todas as permissões de **leitura**

3. **admin**: Acesso completo ao sistema
   - Gerenciar usuários (criar, atualizar, deletar)
   - Todas as permissões de **escrita** e **leitura**

## 📦 Estrutura de Armazenamento

### Localização no Parameter Store

- **Feature Flags**: `/feature-flags/flags/{prefix}/{id}`
- **Usuários**: `/feature-flags/users`

### Estrutura do Parâmetro de Usuários

```json
{
  "usuarios": [
    {
      "id": "gerente@banco.com",
      "nome": "João Silva",
      "permissoes": {
        "leitura": true,
        "escrita": true,
        "admin": true
      },
      "ativo": true
    },
    {
      "id": "desenvolvedor@banco.com",
      "nome": "Maria Santos",
      "permissoes": {
        "leitura": true,
        "escrita": true,
        "admin": false
      },
      "ativo": true
    },
    {
      "id": "analista@banco.com",
      "nome": "Pedro Costa",
      "permissoes": {
        "leitura": true,
        "escrita": false,
        "admin": false
      },
      "ativo": true
    }
  ]
}
```

## 🔑 Autenticação

Todas as requisições à API devem incluir o header `X-User-Id` com o identificador do usuário:

```bash
curl -X GET https://sua-api.amazonaws.com/parameters \
  -H "X-User-Id: gerente@banco.com"
```

## 📝 API de Usuários

### 1. Listar Todos os Usuários

**Permissão necessária**: `leitura`

```bash
GET /users
Headers:
  X-User-Id: gerente@banco.com
```

**Resposta**:
```json
{
  "usuarios": [
    {
      "id": "gerente@banco.com",
      "nome": "João Silva",
      "permissoes": {
        "leitura": true,
        "escrita": true,
        "admin": true
      },
      "ativo": true
    }
  ]
}
```

### 2. Ver Usuário Específico

**Permissão necessária**: `leitura`

```bash
GET /users/{userId}
Headers:
  X-User-Id: gerente@banco.com
```

**Resposta**:
```json
{
  "id": "desenvolvedor@banco.com",
  "nome": "Maria Santos",
  "permissoes": {
    "leitura": true,
    "escrita": true,
    "admin": false
  },
  "ativo": true
}
```

### 3. Criar Novo Usuário

**Permissão necessária**: `admin`

```bash
POST /users
Headers:
  X-User-Id: gerente@banco.com
  Content-Type: application/json

Body:
{
  "id": "novo@banco.com",
  "nome": "Novo Usuário",
  "permissoes": {
    "leitura": true,
    "escrita": false,
    "admin": false
  },
  "ativo": true
}
```

**Resposta**:
```json
{
  "message": "User created successfully",
  "id": "novo@banco.com"
}
```

### 4. Atualizar Usuário

**Permissão necessária**: `admin`

```bash
PUT /users/{userId}
Headers:
  X-User-Id: gerente@banco.com
  Content-Type: application/json

Body:
{
  "nome": "Novo Nome",
  "permissoes": {
    "leitura": true,
    "escrita": true,
    "admin": false
  },
  "ativo": true
}
```

**Resposta**:
```json
{
  "message": "User updated successfully",
  "id": "desenvolvedor@banco.com"
}
```

### 5. Deletar Usuário

**Permissão necessária**: `admin`

```bash
DELETE /users/{userId}
Headers:
  X-User-Id: gerente@banco.com
```

**Resposta**:
```json
{
  "message": "User deleted successfully",
  "id": "desenvolvedor@banco.com"
}
```

## 🏷️ Prefixos Customizados para Feature Flags

Agora é possível organizar feature flags usando prefixos customizados. Os prefixos são sempre criados dentro de `/feature-flags/flags/`.

### Criar Flag com Prefixo

```bash
POST /parameters
Headers:
  X-User-Id: gerente@banco.com
  Content-Type: application/json

Body:
{
  "id": "DARK_MODE",
  "value": "true",
  "type": "BOOLEAN",
  "description": "Modo escuro da interface",
  "prefix": "ui",
  "lastModifiedBy": "gerente@banco.com"
}
```

Isso criará o parâmetro em: `/feature-flags/flags/ui/DARK_MODE`

### Exemplos de Organização com Prefixos

```
/feature-flags/flags/
├── ui/
│   ├── DARK_MODE
│   ├── THEME_COLOR
│   └── SHOW_BANNER
├── api/
│   ├── MAX_TIMEOUT
│   ├── RETRY_COUNT
│   └── CACHE_ENABLED
├── payment/
│   ├── PIX_ENABLED
│   ├── CREDIT_CARD_LIMIT
│   └── INSTALLMENTS_MAX
└── (sem prefixo)
    ├── MAINTENANCE_MODE
    └── DEBUG_ENABLED
```

## 🚨 Códigos de Erro

### Erros de Autorização (403 Forbidden)

```json
{
  "error": "User ID is required in header 'X-User-Id'"
}
```

```json
{
  "error": "User gerente@banco.com not found"
}
```

```json
{
  "error": "User desenvolvedor@banco.com is inactive"
}
```

```json
{
  "error": "User analista@banco.com does not have 'escrita' permission"
}
```

## 💡 Exemplos de Uso

### Exemplo 1: Setup Inicial de Usuários

```python
import requests

API_URL = "https://sua-api.amazonaws.com"
ADMIN_ID = "admin@banco.com"

# Criar usuário admin (precisa ser feito manualmente no Parameter Store primeiro)
# ou via AWS CLI

# Criar usuário desenvolvedor
response = requests.post(
    f"{API_URL}/users",
    headers={
        "X-User-Id": ADMIN_ID,
        "Content-Type": "application/json"
    },
    json={
        "id": "dev@banco.com",
        "nome": "Desenvolvedor",
        "permissoes": {
            "leitura": True,
            "escrita": True,
            "admin": False
        },
        "ativo": True
    }
)
print(response.json())
```

### Exemplo 2: Criar Feature Flag com Prefixo

```python
import requests

API_URL = "https://sua-api.amazonaws.com"
USER_ID = "dev@banco.com"

response = requests.post(
    f"{API_URL}/parameters",
    headers={
        "X-User-Id": USER_ID,
        "Content-Type": "application/json"
    },
    json={
        "id": "MAX_RETRY",
        "value": "3",
        "type": "INTEGER",
        "description": "Máximo de tentativas de retry",
        "prefix": "api",
        "lastModifiedBy": USER_ID
    }
)
print(response.json())
```

### Exemplo 3: Usuário Apenas Leitura

```python
import requests

API_URL = "https://sua-api.amazonaws.com"
READER_ID = "analista@banco.com"

# Listar parâmetros - OK
response = requests.get(
    f"{API_URL}/parameters",
    headers={"X-User-Id": READER_ID}
)
print(response.json())

# Tentar criar parâmetro - ERRO 403
response = requests.post(
    f"{API_URL}/parameters",
    headers={
        "X-User-Id": READER_ID,
        "Content-Type": "application/json"
    },
    json={
        "id": "NEW_FLAG",
        "value": "true",
        "type": "BOOLEAN"
    }
)
# Retorna: {"error": "User analista@banco.com does not have 'escrita' permission"}
```

## 🔧 Configuração Inicial

### Passo 1: Criar Primeiro Usuário Admin via AWS CLI

```bash
aws ssm put-parameter \
  --name "/feature-flags/users" \
  --value '{
    "usuarios": [
      {
        "id": "admin@banco.com",
        "nome": "Administrador",
        "permissoes": {
          "leitura": true,
          "escrita": true,
          "admin": true
        },
        "ativo": true
      }
    ]
  }' \
  --type String \
  --description "Feature flags users" \
  --overwrite
```

### Passo 2: Usar a API

Após criar o primeiro admin, todos os outros usuários podem ser criados via API.

## 📊 Boas Práticas

1. **Separe responsabilidades**: Use prefixos para organizar flags por domínio/módulo
2. **Princípio do menor privilégio**: Dê aos usuários apenas as permissões necessárias
3. **Mantenha usuários inativos**: Use `"ativo": false` ao invés de deletar usuários
4. **Documente permissões**: Mantenha registro de quem tem acesso a quê
5. **Rotacione credenciais**: Atualize IDs de usuários periodicamente
6. **Audite ações**: Use o campo `lastModifiedBy` para rastrear mudanças

## 🔍 Troubleshooting

### Erro: "User ID is required in header 'X-User-Id'"
**Solução**: Adicione o header `X-User-Id` em todas as requisições

### Erro: "User xxx@banco.com not found"
**Solução**: Verifique se o usuário existe usando `GET /users`

### Erro: "User xxx@banco.com is inactive"
**Solução**: Ative o usuário com admin: `PUT /users/{userId}` com `"ativo": true`

### Erro: "User xxx@banco.com does not have 'admin' permission"
**Solução**: Apenas admins podem gerenciar usuários. Peça a um admin para atualizar suas permissões
