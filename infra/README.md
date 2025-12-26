# 🚀 Infrastructure & Deployment

Esta pasta contém arquivos de configuração, deployment e especificações da API.

## 📁 Arquivos

### 📋 Especificação da API

- **[openapi.yaml](openapi.yaml)** - Especificação OpenAPI 3.0
  - Documentação completa da API
  - Schemas de request/response
  - Tipos de dados e validações
  - Exemplos de uso

### 🚀 Scripts de Deploy

- **[deploy.sh](deploy.sh)** - Script de deployment para Linux/Mac
  - Instalação de dependências
  - Criação do pacote ZIP
  - Deploy para AWS Lambda
  - Configuração de API Gateway

### ⚙️ Automação

- **[Makefile](Makefile)** - Comandos de automação
  - Build do projeto
  - Testes
  - Deploy
  - Limpeza

## 🚀 Como Fazer Deploy

### Opção 1: Usando deploy.sh (Linux/Mac)

```bash
cd ../  # Voltar para raiz do projeto
chmod +x infra/deploy.sh
./infra/deploy.sh
```

### Opção 2: Usando Makefile

```bash
cd ../  # Voltar para raiz do projeto
make deploy
```

### Opção 3: Deploy Manual

1. **Instalar dependências**:
```bash
pip install -r requirements.txt -t .
```

2. **Criar pacote**:
```bash
zip -r function.zip . -x "*.git*" "*.pyc" "__pycache__/*" "tests/*"
```

3. **Deploy para Lambda**:
```bash
aws lambda create-function \
  --function-name feature-flag-manager \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR-ACCOUNT:role/lambda-ssm-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip
```

## 📋 Pré-requisitos

### AWS Credentials
```bash
aws configure
```

### IAM Role
O Lambda precisa de uma role com permissões SSM:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameter",
        "ssm:PutParameter",
        "ssm:DescribeParameters"
      ],
      "Resource": "arn:aws:ssm:*:*:parameter/feature-flags/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

## 🔧 Configuração

### Variáveis de Ambiente (Lambda)

Configure as seguintes variáveis de ambiente no Lambda:

```bash
# Opcional: Configurações customizadas
LOG_LEVEL=INFO
AWS_REGION=us-east-1
```

### API Gateway

1. Crie um REST API no API Gateway
2. Configure os seguintes endpoints:
   - `GET /parameters` → Lambda Proxy Integration
   - `POST /parameters` → Lambda Proxy Integration
   - `PUT /parameters/{proxy+}` → Lambda Proxy Integration

3. Configure CORS se necessário:
```json
{
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET,POST,PUT,OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type"
}
```

4. Deploy para um stage (ex: `prod`)

## 📊 OpenAPI Specification

O arquivo `openapi.yaml` contém a especificação completa da API e pode ser usado para:

### 1. Gerar Documentação
```bash
# Usando Swagger UI
docker run -p 80:8080 -e SWAGGER_JSON=/openapi.yaml -v $(pwd)/openapi.yaml:/openapi.yaml swaggerapi/swagger-ui

# Acesse: http://localhost
```

### 2. Gerar SDK Cliente
```bash
# Instalar OpenAPI Generator
npm install @openapitools/openapi-generator-cli -g

# Gerar SDK Python
openapi-generator-cli generate -i openapi.yaml -g python -o client-sdk/

# Gerar SDK JavaScript
openapi-generator-cli generate -i openapi.yaml -g javascript -o client-sdk-js/
```

### 3. Validar Requests
Use ferramentas como Postman, Insomnia ou outros clientes REST para importar o OpenAPI spec e testar a API.

## 🧪 Testando após Deploy

```bash
# Listar parâmetros
curl -X GET https://YOUR-API-GATEWAY-URL/prod/parameters

# Criar parâmetro
curl -X POST https://YOUR-API-GATEWAY-URL/prod/parameters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-flag",
    "value": true,
    "value_type": "boolean",
    "description": "Test flag",
    "domain": "test",
    "enabled": true,
    "modified_by": "admin"
  }'

# Atualizar parâmetro
curl -X PUT https://YOUR-API-GATEWAY-URL/prod/parameters/test-flag \
  -H "Content-Type: application/json" \
  -d '{
    "value": false,
    "modified_by": "admin"
  }'
```

## 🔍 Monitoramento

### CloudWatch Logs
```bash
# Ver logs
aws logs tail /aws/lambda/feature-flag-manager --follow
```

### Métricas
- Invocações
- Erros
- Duração
- Throttles

## 📚 Documentação Relacionada

- [← Voltar para README principal](../README.md)
- [Ver documentação completa](../docs/)
- [Ver eventos de teste](../tests/events/)

## 🆘 Troubleshooting

### Erro: "No module named 'boto3'"
**Solução**: Certifique-se de incluir as dependências no pacote ZIP

### Erro: "Access Denied" ao acessar SSM
**Solução**: Verifique se a IAM role tem as permissões corretas

### Erro: "Internal Server Error"
**Solução**: Verifique os logs no CloudWatch

## 📝 Boas Práticas

1. **Use diferentes stages**: dev, staging, prod
2. **Configure alarmes** no CloudWatch
3. **Versione suas functions** Lambda
4. **Use aliases** para gestão de tráfego
5. **Configure tags** para billing e organização
6. **Habilite X-Ray** para tracing distribuído
