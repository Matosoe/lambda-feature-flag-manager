#!/bin/bash

# Script para inicializar o LocalStack
echo "Inicializando Lambda no LocalStack..."

# Executar comandos dentro do container
docker exec feature-flag-localstack sh -c '
cd /tmp
mkdir -p lambda-package
cd lambda-package

# Copiar código fonte
cp -r /docker-entrypoint-initaws.d/src ./
cp /docker-entrypoint-initaws.d/lambda_function.py ./

# Instalar dependências
pip3 install -q --target . boto3 botocore PyYAML

# Criar ZIP
zip -q -r /tmp/function.zip .

# Criar função Lambda
awslocal lambda create-function \
    --function-name feature-flag-manager \
    --runtime python3.11 \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --handler lambda_function.lambda_handler \
    --timeout 30 \
    --memory-size 512 \
    --zip-file fileb:///tmp/function.zip
'

echo "✓ Lambda criada com sucesso!"

# Criar estrutura inicial de usuários
echo "Criando usuários pré-configurados..."
docker exec feature-flag-localstack sh -c '
awslocal ssm put-parameter \
    --name "/feature-flags/users" \
    --value "{\"usuarios\": [{\"id\": \"admin@local.dev\", \"nome\": \"Admin Local\", \"permissoes\": {\"leitura\": true, \"escrita\": true, \"admin\": true}, \"ativo\": true}, {\"id\": \"dev@local.dev\", \"nome\": \"Desenvolvedor\", \"permissoes\": {\"leitura\": true, \"escrita\": true, \"admin\": false}, \"ativo\": true}, {\"id\": \"analista@local.dev\", \"nome\": \"Analista\", \"permissoes\": {\"leitura\": true, \"escrita\": false, \"admin\": false}, \"ativo\": true}]}" \
    --type String \
    --overwrite
'
echo "✓ Usuários criados com sucesso!"
