# Estrutura Padrão de Parâmetros

## Visão Geral

Cada feature flag (parâmetro) agora possui uma estrutura JSON padronizada que inclui metadados completos para gerenciamento e auditoria.

## Estrutura JSON

```json
{
  "description": "Descrição da feature flag",
  "domain": "Domínio ou área de negócio",
  "last_modified": "2025-12-25T10:30:00.000000",
  "modified_by": "usuario@exemplo.com",
  "enabled": true,
  "value_type": "boolean",
  "value": true
}
```

## Campos

### 1. **description** (string)
- **Descrição**: Descrição detalhada da feature flag
- **Obrigatório**: Não (padrão: string vazia)
- **Exemplo**: `"Habilita novo sistema de pagamentos"`

### 2. **domain** (string)
- **Descrição**: Domínio ou área de negócio à qual a flag pertence
- **Obrigatório**: Não (padrão: string vazia)
- **Exemplo**: `"pagamentos"`, `"user-interface"`, `"backend-services"`

### 3. **last_modified** (string, ISO 8601)
- **Descrição**: Timestamp da última alteração ou criação
- **Obrigatório**: Sim (gerado automaticamente)
- **Formato**: ISO 8601 UTC
- **Exemplo**: `"2025-12-25T10:30:00.000000"`

### 4. **modified_by** (string)
- **Descrição**: Identificador do usuário que criou ou modificou o parâmetro
- **Obrigatório**: Não (padrão: string vazia)
- **Exemplo**: `"admin@exemplo.com"`, `"usuario123"`

### 5. **enabled** (boolean)
- **Descrição**: Indica se a feature flag está ativa ou não
- **Obrigatório**: Não (padrão: `true`)
- **Valores**: `true` ou `false`

### 6. **value_type** (string)
- **Descrição**: Tipo do valor armazenado
- **Obrigatório**: Não (padrão: `"string"`)
- **Valores válidos**:
  - `"boolean"` - Valor booleano (true/false)
  - `"string"` - Texto
  - `"integer"` - Número inteiro
  - `"double"` - Número decimal
  - `"date"` - Data (formato string ISO)
  - `"time"` - Hora (formato string)
  - `"datetime"` - Data e hora (formato string ISO)
  - `"json"` - Objeto JSON ou array

### 7. **value** (any)
- **Descrição**: O valor real da feature flag
- **Obrigatório**: Sim
- **Tipo**: Depende do campo `value_type`
- **Exemplos**:
  - Boolean: `true`, `false`
  - String: `"modo-escuro"`
  - Integer: `100`
  - Double: `3.14`
  - Date: `"2025-12-25"`
  - Time: `"14:30:00"`
  - DateTime: `"2025-12-25T14:30:00Z"`
  - JSON: `{"opcao1": true, "opcao2": "valor"}`

## Exemplos de Uso

### Exemplo 1: Feature Flag Booleana
```json
{
  "name": "dark-mode-enabled",
  "value": true,
  "value_type": "boolean",
  "description": "Habilita o modo escuro na interface",
  "domain": "user-interface",
  "enabled": true,
  "modified_by": "admin@exemplo.com"
}
```

### Exemplo 2: Feature Flag com Valor Numérico
```json
{
  "name": "max-upload-size",
  "value": 10485760,
  "value_type": "integer",
  "description": "Tamanho máximo de upload em bytes (10MB)",
  "domain": "file-management",
  "enabled": true,
  "modified_by": "devops@exemplo.com"
}
```

### Exemplo 3: Feature Flag com Configuração JSON
```json
{
  "name": "payment-config",
  "value": {
    "providers": ["stripe", "paypal"],
    "default_currency": "BRL",
    "timeout_seconds": 30
  },
  "value_type": "json",
  "description": "Configuração do sistema de pagamentos",
  "domain": "payments",
  "enabled": true,
  "modified_by": "admin@exemplo.com"
}
```

### Exemplo 4: Feature Flag Desabilitada
```json
{
  "name": "experimental-feature",
  "value": "beta-mode",
  "value_type": "string",
  "description": "Funcionalidade experimental em desenvolvimento",
  "domain": "experimental",
  "enabled": false,
  "modified_by": "developer@exemplo.com"
}
```

## API Endpoints

### Criar Parâmetro
```bash
POST /parameters
Content-Type: application/json

{
  "name": "minha-flag",
  "value": true,
  "value_type": "boolean",
  "description": "Descrição da flag",
  "domain": "meu-dominio",
  "enabled": true,
  "modified_by": "usuario@exemplo.com"
}
```

### Atualizar Parâmetro
```bash
PUT /parameters/{nome}
Content-Type: application/json

{
  "value": false,
  "description": "Nova descrição",
  "enabled": false,
  "modified_by": "usuario@exemplo.com"
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
      "name": "minha-flag",
      "full_name": "/feature-flags/minha-flag",
      "description": "Descrição da flag",
      "domain": "meu-dominio",
      "last_modified": "2025-12-25T10:30:00.000000",
      "modified_by": "usuario@exemplo.com",
      "enabled": true,
      "value_type": "boolean",
      "value": true
    }
  ]
}
```

## Validações

O sistema valida automaticamente:

1. **Tipo do valor** deve corresponder ao `value_type` especificado
2. **value_type** deve ser um dos tipos válidos
3. **enabled** deve ser booleano quando fornecido
4. **name** não pode conter caractere `/`
5. Campos de texto como `description`, `domain`, `modified_by` devem ser strings

## Retrocompatibilidade

O sistema mantém retrocompatibilidade com parâmetros antigos que não seguem a estrutura JSON. Quando um parâmetro antigo é lido:

- O valor é retornado no campo `value`
- Campos ausentes recebem valores padrão
- `value_type` é definido como `"string"`
- `enabled` é definido como `true`

## Boas Práticas

1. **Sempre especifique o `value_type`** correto para aproveitar a validação de tipos
2. **Use `domain`** para organizar flags por área de negócio
3. **Preencha `modified_by`** para rastreabilidade
4. **Use `description`** detalhada para documentar o propósito da flag
5. **Use `enabled`** para desativar flags temporariamente sem deletá-las
