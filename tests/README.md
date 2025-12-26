# 🧪 Tests

Esta pasta contém os testes e eventos de teste do projeto.

## 📁 Estrutura

```
tests/
├── events/                     # Eventos de teste para Lambda
│   ├── test_event_create.json
│   ├── test_event_update.json
│   ├── test_event_list.json
│   └── test_event_create_*.json
├── test_lambda_handler.py      # Testes do handler
├── test_service.py             # Testes da camada de serviço
└── test_validator.py           # Testes de validação
```

## 🎯 Eventos de Teste

### 📄 Disponíveis em `events/`

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| `test_event_create.json` | POST | Criar flag boolean |
| `test_event_update.json` | PUT | Atualizar flag |
| `test_event_list.json` | GET | Listar todas as flags |
| `test_event_create_integer.json` | POST | Criar flag integer |
| `test_event_create_double.json` | POST | Criar flag double |
| `test_event_create_json.json` | POST | Criar flag JSON complexa |
| `test_event_create_date.json` | POST | Criar flag com data |

## 🚀 Como Usar os Eventos de Teste

### 1. Teste Local com Python

```python
from lambda_function import lambda_handler
import json

# Carregar evento
with open('tests/events/test_event_create.json') as f:
    event = json.load(f)

# Executar
response = lambda_handler(event, None)

# Ver resultado
print(json.dumps(response, indent=2))
```

### 2. Teste com AWS CLI

```bash
# Invocar Lambda remotamente
aws lambda invoke \
  --function-name feature-flag-manager \
  --payload file://tests/events/test_event_create.json \
  response.json

# Ver resposta
cat response.json | jq
```

### 3. Teste com AWS SAM Local

```bash
sam local invoke FeatureFlagFunction \
  --event tests/events/test_event_create.json
```

## 📋 Exemplos de Eventos

### Criar Flag Boolean
```json
{
  "httpMethod": "POST",
  "path": "/parameters",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"name\": \"dark-mode\", \"value\": true, \"value_type\": \"boolean\", \"description\": \"Modo escuro\", \"domain\": \"ui\", \"enabled\": true, \"modified_by\": \"admin@example.com\"}"
}
```

### Listar Todas as Flags
```json
{
  "httpMethod": "GET",
  "path": "/parameters",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null
}
```

### Atualizar Flag
```json
{
  "httpMethod": "PUT",
  "path": "/parameters/dark-mode",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"value\": false, \"enabled\": false, \"modified_by\": \"admin@example.com\"}"
}
```

## 🧪 Executar Testes Unitários

### Instalar dependências de teste
```bash
pip install -r requirements-dev.txt
```

### Executar todos os testes
```bash
pytest
```

### Executar com cobertura
```bash
pytest --cov=src --cov-report=html
```

### Executar testes específicos
```bash
# Apenas testes do validator
pytest tests/test_validator.py

# Apenas testes do service
pytest tests/test_service.py

# Apenas testes do lambda handler
pytest tests/test_lambda_handler.py
```

## 📊 Cobertura de Testes

Os testes cobrem:

- ✅ Validação de entrada
- ✅ Criação de parâmetros
- ✅ Atualização de parâmetros
- ✅ Listagem de parâmetros
- ✅ Tratamento de erros
- ✅ Validação de tipos
- ✅ Retrocompatibilidade

## 🎨 Criando Novos Eventos de Teste

### Template Básico
```json
{
  "httpMethod": "POST|GET|PUT",
  "path": "/parameters/{nome-opcional}",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"campo\": \"valor\"}",
  "isBase64Encoded": false
}
```

### Dicas
1. **body** deve ser uma string JSON escapada
2. **httpMethod** deve ser maiúsculo
3. **path** deve começar com `/`
4. Use `null` para body em requisições GET

## 🔍 Debugging

### Executar com logs detalhados
```python
import logging
logging.basicConfig(level=logging.DEBUG)

from lambda_function import lambda_handler
# ... seu teste
```

### Ver estrutura do evento
```python
import json

with open('tests/events/test_event_create.json') as f:
    event = json.load(f)
    
print(json.dumps(event, indent=2))
```

## 📚 Documentação Relacionada

- [← Voltar para README principal](../README.md)
- [Ver documentação](../docs/)
- [Ver exemplos de uso](../docs/EXAMPLES.md)

## 🆘 Troubleshooting

### Erro: "File not found"
**Solução**: Execute os comandos a partir da raiz do projeto

### Erro: "Module not found"
**Solução**: Instale as dependências: `pip install -r requirements.txt`

### Erro: "Access Denied"
**Solução**: Configure suas credenciais AWS: `aws configure`

## 💡 Boas Práticas

1. **Sempre teste localmente** antes de fazer deploy
2. **Use eventos de teste** para validar mudanças
3. **Mantenha eventos atualizados** com a estrutura da API
4. **Documente casos de teste** especiais
5. **Use nomes descritivos** para arquivos de teste
