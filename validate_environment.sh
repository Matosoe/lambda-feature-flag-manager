#!/bin/bash

# Script de validação do ambiente Docker LocalStack
# Verifica se todos os componentes estão funcionando

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Feature Flag Manager - Validação${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Função para verificar comandos
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "  ${GREEN}✓${NC} $1 instalado"
        return 0
    else
        echo -e "  ${RED}✗${NC} $1 não encontrado"
        return 1
    fi
}

# Função para verificar containers
check_container() {
    if docker ps | grep -q $1; then
        echo -e "  ${GREEN}✓${NC} Container $1 rodando"
        return 0
    else
        echo -e "  ${RED}✗${NC} Container $1 não está rodando"
        return 1
    fi
}

errors=0

# 1. Verificar pré-requisitos
echo -e "${BLUE}1. Verificando pré-requisitos...${NC}"
check_command docker || ((errors++))
check_command docker-compose || check_command "docker compose" || ((errors++))
check_command python || check_command python3 || ((errors++))
check_command make || echo -e "  ${YELLOW}⚠${NC} make não encontrado (opcional)"
echo ""

# 2. Verificar arquivos necessários
echo -e "${BLUE}2. Verificando arquivos...${NC}"
files=(
    "docker-compose.yml"
    "Dockerfile"
    "init-localstack.sh"
    "Makefile"
    "lambda_function.py"
    "src/handler.py"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file existe"
    else
        echo -e "  ${RED}✗${NC} $file não encontrado"
        ((errors++))
    fi
done
echo ""

# 3. Verificar containers
echo -e "${BLUE}3. Verificando containers Docker...${NC}"
if docker ps > /dev/null 2>&1; then
    check_container "localstack" || echo -e "  ${YELLOW}⚠${NC} LocalStack não está rodando (execute 'make up')"
else
    echo -e "  ${RED}✗${NC} Docker não está rodando"
    ((errors++))
fi
echo ""

# 4. Verificar LocalStack
echo -e "${BLUE}4. Verificando LocalStack...${NC}"
if curl -s http://localhost:4566/_localstack/health > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓${NC} LocalStack respondendo em localhost:4566"
    
    # Verificar serviços
    health=$(curl -s http://localhost:4566/_localstack/health)
    if echo $health | grep -q "lambda"; then
        echo -e "  ${GREEN}✓${NC} Serviço Lambda disponível"
    fi
    if echo $health | grep -q "ssm"; then
        echo -e "  ${GREEN}✓${NC} Serviço SSM disponível"
    fi
else
    echo -e "  ${YELLOW}⚠${NC} LocalStack não está acessível (execute 'make up')"
fi
echo ""

# 5. Verificar Lambda
echo -e "${BLUE}5. Verificando Lambda Function...${NC}"
if command -v aws &> /dev/null; then
    if aws --endpoint-url=http://localhost:4566 lambda list-functions 2>/dev/null | grep -q "feature-flag-manager"; then
        echo -e "  ${GREEN}✓${NC} Lambda function 'feature-flag-manager' criada"
        
        # Tentar obter URL
        url=$(aws --endpoint-url=http://localhost:4566 lambda get-function-url-config --function-name feature-flag-manager --query 'FunctionUrl' --output text 2>/dev/null)
        if [ -n "$url" ]; then
            echo -e "  ${GREEN}✓${NC} Function URL configurada"
            echo -e "     URL: $url"
        fi
    else
        echo -e "  ${YELLOW}⚠${NC} Lambda function não encontrada (execute 'make up')"
    fi
else
    echo -e "  ${YELLOW}⚠${NC} AWS CLI não instalado (opcional)"
fi
echo ""

# 6. Verificar parâmetros
echo -e "${BLUE}6. Verificando Parameter Store...${NC}"
if command -v aws &> /dev/null; then
    params=$(aws --endpoint-url=http://localhost:4566 ssm describe-parameters 2>/dev/null | grep -c "Name")
    if [ "$params" -gt 0 ]; then
        echo -e "  ${GREEN}✓${NC} Parameter Store com $params parâmetros"
        
        # Verificar parâmetro de usuários
        if aws --endpoint-url=http://localhost:4566 ssm get-parameter --name /feature-flags/users &> /dev/null; then
            echo -e "  ${GREEN}✓${NC} Parâmetro de usuários existe"
        fi
    else
        echo -e "  ${YELLOW}⚠${NC} Nenhum parâmetro encontrado (execute 'make up')"
    fi
fi
echo ""

# 7. Resumo
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Resumo${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

if [ $errors -eq 0 ]; then
    echo -e "${GREEN}✓ Validação concluída com sucesso!${NC}"
    echo ""
    echo -e "Próximos passos:"
    echo -e "  1. ${BLUE}make up${NC}      - Subir ambiente (se ainda não estiver rodando)"
    echo -e "  2. ${BLUE}make test-api${NC} - Testar API"
    echo -e "  3. ${BLUE}make info${NC}     - Ver informações do ambiente"
    echo ""
    exit 0
else
    echo -e "${RED}✗ Validação encontrou $errors erro(s)${NC}"
    echo ""
    echo -e "Ações recomendadas:"
    echo -e "  1. Verifique se Docker está rodando"
    echo -e "  2. Execute ${BLUE}make build${NC} para buildar as imagens"
    echo -e "  3. Execute ${BLUE}make up${NC} para subir o ambiente"
    echo -e "  4. Execute este script novamente"
    echo ""
    exit 1
fi
