#!/bin/bash

# Script de deploy do site estático para S3

set -e

# Configurações
BUCKET_NAME="${BUCKET_NAME:-feature-flag-web}"
AWS_REGION="${AWS_REGION:-us-east-1}"
AWS_PROFILE="${AWS_PROFILE:-default}"

echo "🚀 Iniciando deploy do site web..."
echo ""
echo "📦 Bucket: $BUCKET_NAME"
echo "🌎 Region: $AWS_REGION"
echo "👤 Profile: $AWS_PROFILE"
echo ""

# Verificar se AWS CLI está instalado
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI não encontrado. Instale: https://aws.amazon.com/cli/"
    exit 1
fi

# Verificar se o bucket existe
echo "🔍 Verificando se o bucket existe..."
if aws s3 ls "s3://$BUCKET_NAME" --profile "$AWS_PROFILE" 2>&1 | grep -q 'NoSuchBucket'; then
    echo "📦 Criando bucket $BUCKET_NAME..."
    aws s3 mb "s3://$BUCKET_NAME" --region "$AWS_REGION" --profile "$AWS_PROFILE"
    
    echo "⚙️  Configurando bucket para hospedagem estática..."
    aws s3 website "s3://$BUCKET_NAME" \
        --index-document index.html \
        --profile "$AWS_PROFILE"
    
    echo "🔓 Configurando política de acesso público..."
    cat > /tmp/bucket-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
        }
    ]
}
EOF
    
    aws s3api put-bucket-policy \
        --bucket "$BUCKET_NAME" \
        --policy file:///tmp/bucket-policy.json \
        --profile "$AWS_PROFILE"
    
    rm /tmp/bucket-policy.json
else
    echo "✅ Bucket já existe"
fi

# Upload dos arquivos
echo ""
echo "📤 Fazendo upload dos arquivos..."
aws s3 sync . "s3://$BUCKET_NAME" \
    --profile "$AWS_PROFILE" \
    --exclude ".git/*" \
    --exclude "*.sh" \
    --exclude "README.md" \
    --exclude ".DS_Store" \
    --delete \
    --cache-control "max-age=3600"

# Configurar tipos de conteúdo
echo "⚙️  Configurando tipos de conteúdo..."
aws s3 cp "s3://$BUCKET_NAME/index.html" "s3://$BUCKET_NAME/index.html" \
    --profile "$AWS_PROFILE" \
    --content-type "text/html" \
    --metadata-directive REPLACE \
    --cache-control "max-age=3600"

aws s3 cp "s3://$BUCKET_NAME/sso.js" "s3://$BUCKET_NAME/sso.js" \
    --profile "$AWS_PROFILE" \
    --content-type "application/javascript" \
    --metadata-directive REPLACE \
    --cache-control "max-age=3600"

# Obter URL do site
WEBSITE_URL=$(aws s3api get-bucket-website --bucket "$BUCKET_NAME" --profile "$AWS_PROFILE" 2>&1 | grep -q 'NoSuchWebsiteConfiguration' && echo "http://$BUCKET_NAME.s3-website-$AWS_REGION.amazonaws.com" || echo "http://$BUCKET_NAME.s3-website-$AWS_REGION.amazonaws.com")

echo ""
echo "✅ Deploy concluído com sucesso!"
echo ""
echo "🌐 URL do site:"
echo "   $WEBSITE_URL"
echo ""
echo "📋 Próximos passos:"
echo "   1. Acesse o site no navegador"
echo "   2. Configure o Redirect URI no Azure AD (se usar SSO real)"
echo "   3. Teste a autenticação"
echo ""

# Abrir no navegador (opcional)
read -p "Deseja abrir o site no navegador? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if command -v xdg-open &> /dev/null; then
        xdg-open "$WEBSITE_URL"
    elif command -v open &> /dev/null; then
        open "$WEBSITE_URL"
    elif command -v start &> /dev/null; then
        start "$WEBSITE_URL"
    else
        echo "Abra manualmente: $WEBSITE_URL"
    fi
fi
