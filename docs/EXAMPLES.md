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
    "name": "dark-mode-enabled",
    "value": true,
    "value_type": "boolean",
    "description": "Habilita o modo escuro na interface do usuário",
    "domain": "user-interface",
    "enabled": true,
    "modified_by": "admin@example.com"
  }'
```

### Resposta
```json
{
  "message": "Parameter created successfully",
  "name": "/feature-flags/dark-mode-enabled",
  "parameter": {
    "name": "dark-mode-enabled",
    "value": true,
    "description": "Habilita o modo escuro na interface do usuário",
    "domain": "user-interface",
    "enabled": true,
    "value_type": "boolean",
    "modified_by": "admin@example.com"
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
    "name": "default-theme",
    "value": "ocean-blue",
    "value_type": "string",
    "description": "Tema padrão da aplicação",
    "domain": "user-interface",
    "enabled": true,
    "modified_by": "design-team@example.com"
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
    "name": "max-upload-size-mb",
    "value": 50,
    "value_type": "integer",
    "description": "Tamanho máximo de upload em megabytes",
    "domain": "file-management",
    "enabled": true,
    "modified_by": "backend-team@example.com"
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
    "name": "payment-gateway-config",
    "value": {
      "providers": ["stripe", "paypal", "mercadopago"],
      "default_provider": "stripe",
      "retry_attempts": 3,
      "timeout_seconds": 30,
      "currencies": ["BRL", "USD", "EUR"]
    },
    "value_type": "json",
    "description": "Configuração completa do gateway de pagamentos",
    "domain": "payments",
    "enabled": true,
    "modified_by": "payment-team@example.com"
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
            Name='/feature-flags/payment-gateway-config',
            WithDecryption=True
        )
        
        param_data = json.loads(response['Parameter']['Value'])
        
        if param_data['enabled']:
            self.config = param_data['value']
        else:
            # Configuração padrão se desabilitado
            self.config = {
                "providers": ["stripe"],
                "default_provider": "stripe",
                "retry_attempts": 1,
                "timeout_seconds": 15,
                "currencies": ["BRL"]
            }
    
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

### Desabilitar uma Feature
```bash
curl -X PUT https://sua-api.amazonaws.com/parameters/dark-mode-enabled \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": false,
    "modified_by": "admin@example.com"
  }'
```

### Alterar Valor e Descrição
```bash
curl -X PUT https://sua-api.amazonaws.com/parameters/max-upload-size-mb \
  -H "Content-Type: application/json" \
  -d '{
    "value": 100,
    "description": "Aumentado para 100MB após upgrade do servidor",
    "modified_by": "devops@example.com"
  }'
```

### Atualizar Configuração JSON Parcialmente
```bash
curl -X PUT https://sua-api.amazonaws.com/parameters/payment-gateway-config \
  -H "Content-Type: application/json" \
  -d '{
    "value": {
      "providers": ["stripe", "paypal", "mercadopago", "pix"],
      "default_provider": "pix",
      "retry_attempts": 5,
      "timeout_seconds": 45,
      "currencies": ["BRL", "USD", "EUR", "ARS"]
    },
    "modified_by": "payment-team@example.com"
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
      "name": "dark-mode-enabled",
      "full_name": "/feature-flags/dark-mode-enabled",
      "description": "Habilita o modo escuro na interface do usuário",
      "domain": "user-interface",
      "last_modified": "2025-12-25T10:30:00.000000",
      "modified_by": "admin@example.com",
      "enabled": true,
      "value_type": "boolean",
      "value": true
    },
    {
      "name": "max-upload-size-mb",
      "full_name": "/feature-flags/max-upload-size-mb",
      "description": "Aumentado para 100MB após upgrade do servidor",
      "domain": "file-management",
      "last_modified": "2025-12-25T15:45:00.000000",
      "modified_by": "devops@example.com",
      "enabled": true,
      "value_type": "integer",
      "value": 100
    },
    {
      "name": "payment-gateway-config",
      "full_name": "/feature-flags/payment-gateway-config",
      "description": "Configuração completa do gateway de pagamentos",
      "domain": "payments",
      "last_modified": "2025-12-25T16:20:00.000000",
      "modified_by": "payment-team@example.com",
      "enabled": true,
      "value_type": "json",
      "value": {
        "providers": ["stripe", "paypal", "mercadopago", "pix"],
        "default_provider": "pix",
        "retry_attempts": 5,
        "timeout_seconds": 45,
        "currencies": ["BRL", "USD", "EUR", "ARS"]
      }
    }
  ]
}
```

### Filtrar por Domínio (no código)
```python
import boto3
import json

def get_flags_by_domain(domain):
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
            
            if param_data.get('domain') == domain:
                flags.append({
                    'name': param['Name'].replace('/feature-flags/', ''),
                    'value': param_data['value'],
                    'enabled': param_data['enabled']
                })
    
    return flags

# Uso
ui_flags = get_flags_by_domain('user-interface')
print(f"Flags de UI: {ui_flags}")
```

---

## Boas Práticas

1. **Use domínios consistentes** para agrupar flags relacionadas
2. **Sempre preencha `modified_by`** para auditoria
3. **Descreva claramente** o propósito da flag
4. **Use `enabled: false`** ao invés de deletar flags temporariamente
5. **Escolha o `value_type` correto** para validação automática
6. **Documente mudanças importantes** na descrição ao atualizar

---

## Troubleshooting

### Erro: "Value must be a boolean when value_type is 'boolean'"
- **Causa**: O valor fornecido não corresponde ao tipo declarado
- **Solução**: Certifique-se que o valor JSON está correto:
  ```json
  {"value": true}  // ✅ Correto
  {"value": "true"}  // ❌ Errado - string ao invés de boolean
  ```

### Erro: "Field 'name' must not contain '/' character"
- **Causa**: O nome contém barras
- **Solução**: Use apenas letras, números e hífens:
  ```json
  {"name": "my-feature"}  // ✅ Correto
  {"name": "my/feature"}  // ❌ Errado
  ```

### Flag não está sendo aplicada
- **Verifique**: O campo `enabled` está `true`?
- **Verifique**: O código está lendo o parâmetro correto?
- **Verifique**: O timestamp `last_modified` indica quando foi a última mudança
