# Exemplos de Uso - Feature Flag Manager

Este documento fornece exemplos práticos de como usar o Feature Flag Manager com diferentes tipos de valores.

## Índice
1. [Feature Flag Booleana](#feature-flag-booleana)
2. [Feature Flag String](#feature-flag-string)
3. [Feature Flag Integer](#feature-flag-integer)
4. [Feature Flag Double](#feature-flag-double)
5. [Feature Flag Date](#feature-flag-date)
6. [Feature Flag JSON](#feature-flag-json)
7. [Atualização de Flags](#atualização-de-flags)
8. [Listagem de Flags](#listagem-de-flags)

---

## Feature Flag Booleana

Ideal para funcionalidades liga/desliga.

### Criar
```bash
curl -X POST https://sua-api.amazonaws.com/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "id": "DARK_MODE_ENABLED",
    "value": "true",
    "type": "BOOLEAN",
    "description": "Habilita o modo escuro na interface do usuário",
    "lastModifiedBy": "admin@example.com"
  }'
```

### Resposta
```json
{
  "message": "Parameter created successfully",
  "id": "DARK_MODE_ENABLED",
  "parameter": {
    "id": "DARK_MODE_ENABLED",
    "value": "true",
    "type": "BOOLEAN",
    "description": "Habilita o modo escuro na interface do usuário",
    "lastModifiedAt": "2026-01-14T10:00:00Z",
    "lastModifiedBy": "admin@example.com"
  }
}
```

---

## Feature Flag String

Para valores textuais ou modos de operação.

### Criar
```bash
curl -X POST https://sua-api.amazonaws.com/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "id": "DEFAULT_THEME",
    "value": "ocean-blue",
    "type": "STRING",
    "description": "Tema padrão da aplicação",
    "lastModifiedBy": "design-team@example.com"
  }'
```

---

## Feature Flag Integer

Para valores numéricos inteiros como limites, contadores, etc.

### Criar
```bash
curl -X POST https://sua-api.amazonaws.com/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "id": "MAX_UPLOAD_SIZE_MB",
    "value": "50",
    "type": "INTEGER",
    "description": "Tamanho máximo de upload em megabytes",
    "lastModifiedBy": "backend-team@example.com"
  }'
```

### Exemplo no Código Python
```python
import boto3
import json

ssm = boto3.client('ssm')

# Obter o parâmetro
response = ssm.get_parameter(
    Name='/feature-flags/max-upload-size-mb',
    WithDecryption=True
)

# Parse o JSON
param_data = json.loads(response['Parameter']['Value'])

# Verificar se está habilitado e usar o valor
if param_data['enabled']:
    max_size = param_data['value']  # 50
    max_bytes = max_size * 1024 * 1024  # Converter para bytes
    print(f"Tamanho máximo: {max_bytes} bytes")
```

---

## Feature Flag Double

Para valores decimais como porcentagens, multiplicadores, etc.

### Criar
```bash
curl -X POST https://sua-api.amazonaws.com/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "discount-multiplier",
    "value": 0.15,
    "value_type": "double",
    "description": "Multiplicador de desconto (15%)",
    "domain": "sales",
    "enabled": true,
    "modified_by": "sales-team@example.com"
  }'
```

### Exemplo no Código Python
```python
import boto3
import json

def calculate_discounted_price(original_price):
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(
        Name='/feature-flags/discount-multiplier',
        WithDecryption=True
    )
    
    param_data = json.loads(response['Parameter']['Value'])
    
    if param_data['enabled']:
        discount = param_data['value']  # 0.15
        final_price = original_price * (1 - discount)
        return final_price
    
    return original_price

# Uso
price = calculate_discounted_price(100.00)  # R$ 85.00
```

---

## Feature Flag Date

Para datas específicas como vencimentos, lançamentos, etc.

### Criar
```bash
curl -X POST https://sua-api.amazonaws.com/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "maintenance-scheduled-date",
    "value": "2025-12-31",
    "value_type": "date",
    "description": "Data da próxima manutenção programada",
    "domain": "operations",
    "enabled": true,
    "modified_by": "ops-team@example.com"
  }'
```

### Exemplo no Código Python
```python
import boto3
import json
from datetime import datetime

ssm = boto3.client('ssm')
response = ssm.get_parameter(
    Name='/feature-flags/maintenance-scheduled-date',
    WithDecryption=True
)

param_data = json.loads(response['Parameter']['Value'])

if param_data['enabled']:
    maintenance_date = datetime.fromisoformat(param_data['value'])
    days_until = (maintenance_date - datetime.now()).days
    
    if days_until <= 7:
        print(f"⚠️ Manutenção em {days_until} dias!")
```

---

## Feature Flag JSON

Para configurações complexas com múltiplos valores.

### Criar
```bash
curl -X POST https://sua-api.amazonaws.com/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "id": "PAYMENT_GATEWAY_CONFIG",
    "value": "{\"providers\": [\"stripe\", \"paypal\", \"mercadopago\"], \"default_provider\": \"stripe\", \"retry_attempts\": 3, \"timeout_seconds\": 30, \"currencies\": [\"BRL\", \"USD\", \"EUR\"]}",
    "type": "JSON",
    "description": "Configuração completa do gateway de pagamentos",
    "lastModifiedBy": "payment-team@example.com"
  }'
```

### Exemplo no Código Python
```python
import boto3
import json

class PaymentGateway:
    def __init__(self):
        ssm = boto3.client('ssm')
        response = ssm.get_parameter(
            Name='/feature-flags/PAYMENT_GATEWAY_CONFIG',
            WithDecryption=True
        )
        
        param_data = json.loads(response['Parameter']['Value'])
        
        # Parse o valor JSON armazenado como string
        self.config = json.loads(param_data['value'])
    
    def process_payment(self, amount, currency):
        if currency not in self.config['currencies']:
            raise ValueError(f"Moeda {currency} não suportada")
        
        provider = self.config['default_provider']
        timeout = self.config['timeout_seconds']
        
        # Processar pagamento...
        print(f"Processando {amount} {currency} via {provider}")

# Uso
gateway = PaymentGateway()
gateway.process_payment(100.00, "BRL")
```

---

## Atualização de Flags

### Alterar Valor de uma Feature
```bash
curl -X PUT https://sua-api.amazonaws.com/parameters/DARK_MODE_ENABLED \
  -H "Content-Type: application/json" \
  -d '{
    "value": "false",
    "lastModifiedBy": "admin@example.com"
  }'
```

### Alterar Valor e Descrição
```bash
curl -X PUT https://sua-api.amazonaws.com/parameters/MAX_UPLOAD_SIZE_MB \
  -H "Content-Type: application/json" \
  -d '{
    "value": "100",
    "description": "Aumentado para 100MB após upgrade do servidor",
    "lastModifiedBy": "devops@example.com"
  }'
```

### Atualizar Configuração JSON Parcialmente
```bash
curl -X PUT https://sua-api.amazonaws.com/parameters/PAYMENT_GATEWAY_CONFIG \
  -H "Content-Type: application/json" \
  -d '{
    "value": "{\"providers\": [\"stripe\", \"paypal\", \"mercadopago\", \"pix\"], \"default_provider\": \"pix\", \"retry_attempts\": 5, \"timeout_seconds\": 45, \"currencies\": [\"BRL\", \"USD\", \"EUR\", \"ARS\"]}",
    "lastModifiedBy": "payment-team@example.com"
  }'
```

---

## Listagem de Flags

### Listar Todas as Flags
```bash
curl -X GET https://sua-api.amazonaws.com/parameters
```

### Resposta
```json
{
  "parameters": [
    {
      "id": "DARK_MODE_ENABLED",
      "value": "true",
      "type": "BOOLEAN",
      "description": "Habilita o modo escuro na interface do usuário",
      "lastModifiedAt": "2026-01-14T10:30:00Z",
      "lastModifiedBy": "admin@example.com"
    },
    {
      "id": "MAX_UPLOAD_SIZE_MB",
      "value": "100",
      "type": "INTEGER",
      "description": "Aumentado para 100MB após upgrade do servidor",
      "lastModifiedAt": "2026-01-14T15:45:00Z",
      "lastModifiedBy": "devops@example.com",
      "previousVersion": {
        "value": "50",
        "modifiedAt": "2026-01-10T10:00:00Z",
        "modifiedBy": "devops@example.com"
      }
    },
    {
      "id": "PAYMENT_GATEWAY_CONFIG",
      "value": "{\"providers\": [\"stripe\", \"paypal\", \"mercadopago\", \"pix\"], \"default_provider\": \"pix\", \"retry_attempts\": 5, \"timeout_seconds\": 45, \"currencies\": [\"BRL\", \"USD\", \"EUR\", \"ARS\"]}",
      "type": "JSON",
      "description": "Configuração completa do gateway de pagamentos",
      "lastModifiedAt": "2026-01-14T16:20:00Z",
      "lastModifiedBy": "payment-team@example.com",
      "previousVersion": {
        "value": "{\"providers\": [\"stripe\", \"paypal\", \"mercadopago\"], \"default_provider\": \"stripe\", \"retry_attempts\": 3, \"timeout_seconds\": 30, \"currencies\": [\"BRL\", \"USD\", \"EUR\"]}",
        "modifiedAt": "2026-01-12T14:00:00Z",
        "modifiedBy": "payment-team@example.com"
      }
    }
  ]
}
```

### Filtrar Programaticamente (no código)
```python
import boto3
import json

def get_flags_by_prefix(prefix):
    ssm = boto3.client('ssm')
    
    # Listar todos os parâmetros
    paginator = ssm.get_paginator('describe_parameters')
    pages = paginator.paginate(
        ParameterFilters=[{
            'Key': 'Name',
            'Option': 'BeginsWith',
            'Values': ['/feature-flags']
        }]
    )
    
    flags = []
    for page in pages:
        for param in page['Parameters']:
            response = ssm.get_parameter(
                Name=param['Name'],
                WithDecryption=True
            )
            param_data = json.loads(response['Parameter']['Value'])
            
            if param_data.get('id', '').startswith(prefix):
                flags.append({
                    'id': param_data['id'],
                    'value': param_data['value'],
                    'type': param_data['type']
                })
    
    return flags

# Uso
max_flags = get_flags_by_prefix('MAX_')
print(f"Flags MAX_*: {max_flags}")
```

---

## Boas Práticas

1. **Use IDs descritivos** em UPPER_SNAKE_CASE para fácil identificação
2. **Sempre preencha `lastModifiedBy`** para auditoria
3. **Descreva claramente** o propósito do parâmetro
4. **Escolha o `type` correto** para validação automática
5. **O sistema mantém automaticamente** o histórico da versão anterior

---

## Troubleshooting

### Erro: "Value must be a string"
- **Causa**: O valor fornecido não é uma string
- **Solução**: Todos os valores devem ser strings no formato JSON:
  ```json
  {"value": "true"}  // ✅ Correto para boolean
  {"value": "100"}   // ✅ Correto para integer
  {"value": true}    // ❌ Errado - deve ser string
  ```

### Erro: "Field 'id' is required"
- **Causa**: O ID não foi fornecido
- **Solução**: Sempre inclua um ID válido:
  ```json
  {"id": "MY_FEATURE"}  // ✅ Correto
  {"name": "my-feature"}  // ❌ Errado - use 'id'
  ```

### Parâmetro não está sendo aplicado
- **Verifique**: O código está lendo o parâmetro correto?
- **Verifique**: O timestamp `lastModifiedAt` indica quando foi a última mudança
- **Verifique**: O `type` está correto e o valor está sendo parseado adequadamente
