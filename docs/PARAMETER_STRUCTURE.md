# Estrutura Padrão de Parâmetros

## Visão Geral

Cada feature flag (parâmetro) agora possui uma estrutura JSON padronizada que inclui metadados completos para gerenciamento e auditoria.

## Estrutura JSON

```json
{
  "id": "MAX_RETRY_COUNT",
  "value": "5",
  "type": "INTEGER",
  "description": "Número máximo de tentativas de retry",
  "lastModifiedAt": "2026-01-07T10:30:00Z",
  "lastModifiedBy": "joao.silva",
  "previousVersion": {
    "value": "3",
    "modifiedAt": "2026-01-05T08:00:00Z",
    "modifiedBy": "maria.santos"
  }
}
```

## Campos

### 1. **id** (string)
- **Descrição**: Identificador único do parâmetro
- **Obrigatório**: Sim
- **Exemplo**: `"MAX_RETRY_COUNT"`, `"DARK_MODE_ENABLED"`

### 2. **value** (string)
- **Descrição**: O valor real da feature flag (sempre armazenado como string)
- **Obrigatório**: Sim
- **Exemplos**:
  - Boolean: `"true"`, `"false"`
  - String: `"modo-escuro"`
  - Integer: `"100"`
  - Double: `"3.14"`
  - Date: `"2025-12-25"`
  - Time: `"14:30:00"`
  - DateTime: `"2025-12-25T14:30:00Z"`
  - JSON: `"{\"opcao1\": true, \"opcao2\": \"valor\"}"`

### 3. **type** (string)
- **Descrição**: Tipo do valor armazenado
- **Obrigatório**: Sim
- **Valores válidos**:
  - `"BOOLEAN"` - Valor booleano (true/false)
  - `"STRING"` - Texto
  - `"INTEGER"` - Número inteiro
  - `"DOUBLE"` - Número decimal
  - `"DATE"` - Data (formato string ISO)
  - `"TIME"` - Hora (formato string)
  - `"DATETIME"` - Data e hora (formato string ISO)
  - `"JSON"` - Objeto JSON ou array

### 4. **description** (string)
- **Descrição**: Descrição detalhada da feature flag
- **Obrigatório**: Não (padrão: string vazia)
- **Exemplo**: `"Número máximo de tentativas de retry"`

### 5. **lastModifiedAt** (string, ISO 8601)
- **Descrição**: Timestamp da última alteração ou criação
- **Obrigatório**: Sim (gerado automaticamente)
- **Formato**: ISO 8601 UTC com Z
- **Exemplo**: `"2026-01-07T10:30:00Z"`

### 6. **lastModifiedBy** (string)
- **Descrição**: Identificador do usuário que criou ou modificou o parâmetro
- **Obrigatório**: Não (padrão: string vazia)
- **Exemplo**: `"joao.silva"`, `"admin@exemplo.com"`

### 7. **previousVersion** (object)
- **Descrição**: Versão anterior do parâmetro para histórico de mudanças
- **Obrigatório**: Não (ausente na criação)
- **Campos**:
  - `value` (string): Valor anterior
  - `modifiedAt` (string): Timestamp da modificação anterior
  - `modifiedBy` (string): Usuário que fez a modificação anterior
- **Exemplo**: 
  ```json
  {
    "value": "3",
    "modifiedAt": "2026-01-05T08:00:00Z",
    "modifiedBy": "maria.santos"
  }
  ```

## Exemplos de Uso

### Exemplo 1: Feature Flag Booleana
```json
{
  "id": "DARK_MODE_ENABLED",
  "value": "true",
  "type": "BOOLEAN",
  "description": "Habilita o modo escuro na interface",
  "lastModifiedAt": "2026-01-14T10:00:00Z",
  "lastModifiedBy": "admin@exemplo.com"
}
```

### Exemplo 2: Feature Flag com Valor Numérico
```json
{
  "id": "MAX_UPLOAD_SIZE",
  "value": "10485760",
  "type": "INTEGER",
  "description": "Tamanho máximo de upload em bytes (10MB)",
  "lastModifiedAt": "2026-01-14T11:00:00Z",
  "lastModifiedBy": "devops@exemplo.com"
}
```

### Exemplo 3: Feature Flag com Configuração JSON
```json
{
  "id": "PAYMENT_CONFIG",
  "value": "{\"providers\": [\"stripe\", \"paypal\"], \"default_currency\": \"BRL\", \"timeout_seconds\": 30}",
  "type": "JSON",
  "description": "Configuração do sistema de pagamentos",
  "lastModifiedAt": "2026-01-14T12:00:00Z",
  "lastModifiedBy": "admin@exemplo.com",
  "previousVersion": {
    "value": "{\"providers\": [\"stripe\"], \"default_currency\": \"BRL\", \"timeout_seconds\": 15}",
    "modifiedAt": "2026-01-10T09:00:00Z",
    "modifiedBy": "tech.lead"
  }
}
```

### Exemplo 4: Feature Flag com Histórico de Versão
```json
{
  "id": "EXPERIMENTAL_FEATURE",
  "value": "beta-mode",
  "type": "STRING",
  "description": "Funcionalidade experimental em desenvolvimento",
  "lastModifiedAt": "2026-01-14T13:00:00Z",
  "lastModifiedBy": "developer@exemplo.com",
  "previousVersion": {
    "value": "alpha-mode",
    "modifiedAt": "2026-01-12T10:00:00Z",
    "modifiedBy": "developer@exemplo.com"
  }
}
```

## API Endpoints

### Criar Parâmetro
```bash
POST /parameters
Content-Type: application/json

{
  "id": "MINHA_FLAG",
  "value": "true",
  "type": "BOOLEAN",
  "description": "Descrição da flag",
  "lastModifiedBy": "usuario@exemplo.com"
}
```

### Atualizar Parâmetro
```bash
PUT /parameters/{id}
Content-Type: application/json

{
  "value": "false",
  "description": "Nova descrição",
  "lastModifiedBy": "usuario@exemplo.com"
}
```

### Listar Parâmetros
```bash
GET /parameters
```

Resposta:
```json
{
  "parameters": [
    {
      "id": "MINHA_FLAG",
      "value": "false",
      "type": "BOOLEAN",
      "description": "Nova descrição",
      "lastModifiedAt": "2026-01-14T14:00:00Z",
      "lastModifiedBy": "usuario@exemplo.com",
      "previousVersion": {
        "value": "true",
        "modifiedAt": "2026-01-14T10:00:00Z",
        "modifiedBy": "usuario@exemplo.com"
      }
    }
  ]
}
```

## Validações

O sistema valida automaticamente:

1. **id** é obrigatório e deve ser uma string válida
2. **value** é obrigatório e deve ser uma string
3. **type** deve ser um dos tipos válidos (BOOLEAN, STRING, INTEGER, DOUBLE, DATE, TIME, DATETIME, JSON)
4. **description** e **lastModifiedBy** devem ser strings quando fornecidos
5. **lastModifiedAt** é gerado automaticamente no formato ISO 8601
6. **previousVersion** é opcional e, quando presente, deve conter os campos value, modifiedAt e modifiedBy

## Retrocompatibilidade

O sistema mantém retrocompatibilidade com parâmetros antigos que não seguem a estrutura JSON. Quando um parâmetro antigo é lido:

- O valor é retornado no campo `value` como string
- Campos ausentes recebem valores padrão
- `type` é definido como `"STRING"`
- `lastModifiedAt` usa o timestamp do Parameter Store
- `previousVersion` não é incluído

## Boas Práticas

1. **Use IDs descritivos** em UPPER_SNAKE_CASE (ex: MAX_RETRY_COUNT, DARK_MODE_ENABLED)
2. **Sempre especifique o `type`** correto para aproveitar a validação de tipos
3. **Preencha `lastModifiedBy`** para rastreabilidade de mudanças
4. **Use `description`** detalhada para documentar o propósito do parâmetro
5. **O sistema mantém automaticamente** o histórico da versão anterior em `previousVersion`
