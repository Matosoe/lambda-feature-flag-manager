#!/bin/bash

echo "Atualizando código da Lambda..."

docker exec feature-flag-localstack sh -c '
cd /tmp
rm -rf lambda-package
mkdir -p lambda-package
cd lambda-package

# Copiar código fonte atualizado
cp -r /docker-entrypoint-initaws.d/src ./
cp /docker-entrypoint-initaws.d/lambda_function.py ./

# Instalar dependências
pip3 install -q --target . boto3 botocore PyYAML 2>/dev/null

# Criar ZIP
zip -q -r /tmp/function.zip .

# Atualizar função Lambda
awslocal lambda update-function-code \
    --function-name feature-flag-manager \
    --zip-file fileb:///tmp/function.zip
'

echo "✓ Lambda atualizada com sucesso!"
