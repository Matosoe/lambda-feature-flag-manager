# Infraestrutura Local

Este diretório contém a configuração para executar a infraestrutura localmente usando Docker e LocalStack.

## Pré-requisitos

- Docker
- Docker Compose

## Serviços

A infraestrutura local utiliza **LocalStack** para simular os seguintes serviços AWS:
- **S3**: Armazenamento de objetos
- **Lambda**: Execução de funções serverless
- **API Gateway**: Gateway de APIs
- **IAM**: Gerenciamento de identidades e acessos
- **CloudFormation**: Infraestrutura como código

## Como usar

### Iniciar o ambiente

```bash
./up.sh
```

Este script irá:
1. Criar o diretório de dados local (se não existir)
2. Subir o container do LocalStack
3. Aguardar a inicialização dos serviços
4. Exibir informações sobre os serviços disponíveis

### Parar o ambiente

```bash
./down.sh
```

Este script irá parar e remover os containers.

### Verificar logs

```bash
docker-compose logs -f
```

### Acessar serviços

- **LocalStack Gateway**: http://localhost:4566

### Dados persistidos

Os dados do LocalStack são persistidos no diretório `localstack-data/`. Para limpar completamente o ambiente:

```bash
./down.sh
rm -rf localstack-data
```

## AWS CLI com LocalStack

Para usar o AWS CLI com LocalStack, configure o endpoint:

```bash
aws --endpoint-url=http://localhost:4566 s3 ls
aws --endpoint-url=http://localhost:4566 lambda list-functions
```

Ou configure um profile no `~/.aws/config`:

```ini
[profile localstack]
region = us-east-1
output = json
endpoint_url = http://localhost:4566
```

E use:

```bash
aws --profile localstack s3 ls
```

## Troubleshooting

### Container não inicia

Verifique se as portas 4566 e 4510-4559 não estão em uso:

```bash
netstat -ano | findstr :4566
```

### Logs de erro

```bash
docker-compose logs localstack
```

### Reiniciar completamente

```bash
./down.sh
rm -rf localstack-data
./up.sh
```
