# Guia Rápido - Feature Flag Manager

## 🚀 Início Rápido

### Criar sua primeira feature flag

```bash
curl -X POST https://sua-api.amazonaws.com/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "id": "MINHA_PRIMEIRA_FLAG",
    "value": "true",
    "type": "BOOLEAN",
    "description": "Minha primeira feature flag",
    "lastModifiedBy": "seu-email@exemplo.com"
  }'
```

### Listar todas as flags

```bash
curl -X GET https://sua-api.amazonaws.com/parameters
```

### Atualizar uma flag

```bash
curl -X PUT https://sua-api.amazonaws.com/parameters/MINHA_PRIMEIRA_FLAG \
  -H "Content-Type: application/json" \
  -d '{
    "value": "false",
    "lastModifiedBy": "seu-email@exemplo.com"
  }'
```

## 📋 Estrutura Básica

Toda feature flag possui 7 campos principais:

| Campo | Tipo | Obrigatório | Descrição |
| ----- | ---- | ----------- | --------- ||
| `id` | string | Sim | Identificador único |
| `value` | string | Sim | Valor (sempre string) |
| `type` | string | Sim | Tipo do valor |
| `description` | string | Não | Descrição da flag |
| `lastModifiedAt` | string | Sim* | Timestamp (auto) |
| `lastModifiedBy` | string | Não | Email do usuário |
| `previousVersion` | object | Não | Versão anterior |

*Gerado automaticamente

## 🎨 Tipos Suportados

```
BOOLEAN   → "true", "false"
STRING    → "texto qualquer"
INTEGER   → "42"
DOUBLE    → "3.14"
DATE      → "2025-12-25"
TIME      → "14:30:00"
DATETIME  → "2025-12-25T14:30:00Z"
JSON      → "{\"chave\": \"valor\"}" ou "[\"array\"]"
```

**Importante**: Todos os valores são armazenados como strings.

## 💡 Exemplos Rápidos

### Boolean (On/Off)
```json
{
  "id": "DARK_MODE",
  "value": "true",
  "type": "BOOLEAN"
}
```

### Integer (Limites)
```json
{
  "id": "MAX_UPLOAD_MB",
  "value": "50",
  "type": "INTEGER"
}
```

### JSON (Configurações)
```json
{
  "id": "API_CONFIG",
  "value": "{\"timeout\": 30, \"retry\": 3}",
  "type": "JSON"
}
```

## 🔍 Usar no Código Python

```python
import boto3
import json

def get_flag(flag_id):
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name=f'/feature-flags/{flag_id}',
        WithDecryption=True
    )
    
    # Parse JSON
    flag_data = json.loads(response['Parameter']['Value'])
    
    # Retornar valor parseado de acordo com o tipo
    value = flag_data['value']
    flag_type = flag_data['type']
    
    if flag_type == 'BOOLEAN':
        return value.lower() == 'true'
    elif flag_type == 'INTEGER':
        return int(value)
    elif flag_type == 'DOUBLE':
        return float(value)
    elif flag_type == 'JSON':
        return json.loads(value)
    else:
        return value

# Usar
if get_flag('DARK_MODE'):
    print("Modo escuro ativado!")
```

## 📝 Convenções de Naming

Organize seus IDs usando prefixos:

- `USER_*` - Interface do usuário (ex: USER_DARK_MODE)
- `API_*` - APIs e serviços backend (ex: API_TIMEOUT)
- `PAY_*` - Sistema de pagamentos (ex: PAY_MAX_AMOUNT)
- `INFRA_*` - Infraestrutura (ex: INFRA_CACHE_TTL)
- `EXP_*` - Features experimentais (ex: EXP_NEW_CHECKOUT)
- `OPS_*` - Operações/DevOps (ex: OPS_MAINTENANCE_MODE)
- `SEC_*` - Segurança (ex: SEC_MFA_ENABLED)
- `ANALYTICS_*` - Analytics (ex: ANALYTICS_TRACKING)

## ✅ Checklist de Criação

Ao criar uma feature flag, sempre:

- [ ] Escolha um ID descritivo (use UPPER_SNAKE_CASE)
- [ ] Defina o `type` correto
- [ ] Adicione uma `description` clara
- [ ] Preencha `lastModifiedBy` com seu identificador
- [ ] Garanta que `value` é uma string

## ⚠️ Boas Práticas

### ✅ Faça

- Use IDs descritivos: `ENABLE_NEW_CHECKOUT`
- Documente o propósito na `description`
- Use prefixos para agrupar flags relacionadas
- Sempre preencha `lastModifiedBy`
- Lembre que todos os valores são strings

### ❌ Não Faça

- IDs genéricos: `FLAG1`, `TEST`
- Esquecer a `description`
- Usar tipo errado: STRING quando deveria ser INTEGER
- Deletar flags sem documentar o motivo

## 🐛 Troubleshooting

### Erro: "Value must be a string"
**Problema**: Valor não é string
```json
// ❌ Errado
{"value": true, "type": "BOOLEAN"}

// ✅ Correto
{"value": "true", "type": "BOOLEAN"}
```

### Erro: "Field 'id' is required"
**Problema**: ID ausente
```json
// ❌ Errado
{"name": "my-flag"}

// ✅ Correto
{"id": "MY_FLAG"}
```

### Flag não aplica
**Verifique**:
1. ID do parâmetro está correto?
2. Tipo de parse está adequado ao `type`?
3. Código está lendo o campo correto?

## 📚 Documentação Completa

- 📖 Estrutura detalhada: [PARAMETER_STRUCTURE.md](PARAMETER_STRUCTURE.md)
- 💻 Exemplos de código: [EXAMPLES.md](EXAMPLES.md)
- 🏗️ Arquitetura: [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)
- � Especificação OpenAPI: [../infra/openapi.yaml](../infra/openapi.yaml)

## 🆘 Ajuda Rápida

```bash
# Ver todos os parâmetros
aws ssm describe-parameters --parameter-filters "Key=Name,Option=BeginsWith,Values=/feature-flags"

# Ver valor de uma flag
aws ssm get-parameter --name /feature-flags/MY_FLAG --with-decryption

# Deletar uma flag
aws ssm delete-parameter --name /feature-flags/MY_FLAG
```

## 🎯 Próximos Passos

1. Crie sua primeira feature flag
2. Teste listar todas as flags
3. Experimente atualizar uma flag
4. Integre no seu código
5. Organize flags por domínio
6. Configure CI/CD para deploy automático

---

**Dica**: Comece simples com flags booleanas e evolua para tipos mais complexos conforme necessário!
