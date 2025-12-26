# Guia Rápido - Feature Flag Manager

## 🚀 Início Rápido

### Criar sua primeira feature flag

```bash
curl -X POST https://sua-api.amazonaws.com/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "minha-primeira-flag",
    "value": true,
    "value_type": "boolean",
    "description": "Minha primeira feature flag",
    "domain": "geral",
    "enabled": true,
    "modified_by": "seu-email@exemplo.com"
  }'
```

### Listar todas as flags

```bash
curl -X GET https://sua-api.amazonaws.com/parameters
```

### Atualizar uma flag

```bash
curl -X PUT https://sua-api.amazonaws.com/parameters/minha-primeira-flag \
  -H "Content-Type: application/json" \
  -d '{
    "value": false,
    "modified_by": "seu-email@exemplo.com"
  }'
```

## 📋 Estrutura Básica

Toda feature flag possui 7 campos:

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `description` | string | Não | Descrição da flag |
| `domain` | string | Não | Área de negócio |
| `last_modified` | string | Sim* | Timestamp (auto) |
| `modified_by` | string | Não | Email do usuário |
| `enabled` | boolean | Não | Se está ativa (padrão: true) |
| `value_type` | string | Não | Tipo do valor (padrão: string) |
| `value` | any | Sim | Valor da flag |

*Gerado automaticamente

## 🎨 Tipos Suportados

```
boolean   → true, false
string    → "texto qualquer"
integer   → 42
double    → 3.14
date      → "2025-12-25"
time      → "14:30:00"
datetime  → "2025-12-25T14:30:00Z"
json      → {"chave": "valor"} ou ["array"]
```

## 💡 Exemplos Rápidos

### Boolean (On/Off)
```json
{
  "name": "dark-mode",
  "value": true,
  "value_type": "boolean"
}
```

### Integer (Limites)
```json
{
  "name": "max-upload-mb",
  "value": 50,
  "value_type": "integer"
}
```

### JSON (Configurações)
```json
{
  "name": "api-config",
  "value": {
    "timeout": 30,
    "retry": 3
  },
  "value_type": "json"
}
```

## 🔍 Usar no Código Python

```python
import boto3
import json

def get_flag(flag_name):
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name=f'/feature-flags/{flag_name}',
        WithDecryption=True
    )
    
    # Parse JSON
    flag_data = json.loads(response['Parameter']['Value'])
    
    # Verificar se está habilitada
    if not flag_data.get('enabled', True):
        return None
    
    return flag_data['value']

# Usar
if get_flag('dark-mode'):
    print("Modo escuro ativado!")
```

## 📝 Domínios Sugeridos

Organize suas flags por domínio:

- `user-interface` - Interface do usuário
- `backend` - Serviços backend
- `payments` - Sistema de pagamentos
- `infrastructure` - Infraestrutura
- `experimental` - Features experimentais
- `operations` - Operações/DevOps
- `security` - Segurança
- `analytics` - Analytics

## ✅ Checklist de Criação

Ao criar uma feature flag, sempre:

- [ ] Escolha um nome descritivo (use kebab-case)
- [ ] Defina o `value_type` correto
- [ ] Adicione uma `description` clara
- [ ] Defina o `domain` apropriado
- [ ] Preencha `modified_by` com seu email
- [ ] Defina `enabled: true` para ativar

## ⚠️ Boas Práticas

### ✅ Faça

- Use nomes descritivos: `enable-new-checkout`
- Documente o propósito na `description`
- Agrupe por `domain` relacionado
- Sempre preencha `modified_by`
- Use `enabled: false` para desabilitar temporariamente

### ❌ Não Faça

- Nomes genéricos: `flag1`, `test`
- Esquecer a `description`
- Usar tipo errado: string quando deveria ser boolean
- Deletar flags sem documentar o motivo

## 🐛 Troubleshooting

### Erro: "Value must be a boolean"
**Problema**: Tipo não corresponde
```json
// ❌ Errado
{"value": "true", "value_type": "boolean"}

// ✅ Correto
{"value": true, "value_type": "boolean"}
```

### Erro: "Field 'name' must not contain '/'"
**Problema**: Nome com barra
```json
// ❌ Errado
{"name": "user/dark-mode"}

// ✅ Correto
{"name": "user-dark-mode"}
```

### Flag não aplica
**Verifique**:
1. `enabled` está `true`?
2. Nome do parâmetro está correto?
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
aws ssm get-parameter --name /feature-flags/minha-flag --with-decryption

# Deletar uma flag
aws ssm delete-parameter --name /feature-flags/minha-flag
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
