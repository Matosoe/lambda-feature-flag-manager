# Feature Flag Manager - Ambiente Local

Sistema de gerenciamento de feature flags com suporte a usuários e permissões, rodando completamente local com LocalStack.

## 🚀 Início Rápido

### Pré-requisitos

- Docker e Docker Compose
- Git Bash (Windows) ou Bash (Linux/Mac)
- Python 3.11+ (apenas para testes locais opcionais)

### Subir o Ambiente

```bash
# Buildar as imagens
./build.sh

# Subir LocalStack + Lambda
./up.sh
```

O comando `./up.sh` irá:
- Subir o LocalStack com Lambda e Parameter Store
- Criar a função Lambda automaticamente
- Criar 3 usuários com diferentes permissões
- Criar 4 feature flags de exemplo

### Acessar a API

Após subir o ambiente, você terá uma Lambda Function URL disponível (será exibida no terminal).

Exemplo:
```
http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations
```

## 📖 Comandos Disponíveis

```bash
./help.sh          # Mostra todos os comandos
./build.sh         # Builda as imagens Docker
./up.sh            # Sobe o ambiente
./down.sh          # Para o ambiente
./restart.sh       # Reinicia o ambiente
./logs.sh          # Ver logs do LocalStack
./logs-lambda.sh   # Ver logs da Lambda
./clean.sh         # Remove tudo (containers, volumes, dados)
./info.sh          # Mostra informações do ambiente
./test-api.sh      # Executa testes básicos na API
./test-python.sh   # Executa testes Python completos
./validate.sh      # Valida o ambiente
```

## 👥 Usuários Pré-configurados

O ambiente já vem com 3 usuários:

| Email                | Permissões | Descrição                                      |
| -------------------- | ---------- | ---------------------------------------------- |
| `admin@local.dev`    | Admin      | Pode gerenciar usuários, criar e alterar flags |
| `dev@local.dev`      | Escrita    | Pode criar e alterar flags                     |
| `analista@local.dev` | Leitura    | Pode apenas visualizar flags                   |

## 🚩 Feature Flags Pré-criadas

- `/feature-flags/flags/ui/DARK_MODE` - Boolean para modo escuro
- `/feature-flags/flags/api/MAX_RETRY` - Integer com número de retries
- `/feature-flags/flags/config/API_TIMEOUT` - Double com timeout
- `/feature-flags/flags/MAINTENANCE_MODE` - Boolean global

## 📝 Exemplos de Uso

### Listar todos os parâmetros

```bash
curl -X GET "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters" \
  -H "X-User-Id: dev@local.dev"
```

### Obter parâmetro específico

```bash
curl -X GET "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters/DARK_MODE" \
  -H "X-User-Id: dev@local.dev"
```

### Criar novo parâmetro

```bash
curl -X POST "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters" \
  -H "X-User-Id: dev@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "NEW_FEATURE",
    "value": "true",
    "type": "BOOLEAN",
    "description": "Nova feature em desenvolvimento",
    "lastModifiedBy": "dev@local.dev"
  }'
```

### Criar parâmetro com prefixo customizado

```bash
curl -X POST "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters" \
  -H "X-User-Id: dev@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "BUTTON_COLOR",
    "value": "#FF5733",
    "type": "STRING",
    "description": "Cor do botão principal",
    "prefix": "design",
    "lastModifiedBy": "dev@local.dev"
  }'
```

### Atualizar parâmetro

```bash
curl -X PUT "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters/DARK_MODE" \
  -H "X-User-Id: dev@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "value": "false",
    "description": "Modo escuro desabilitado temporariamente",
    "lastModifiedBy": "dev@local.dev"
  }'
```

### Deletar parâmetro

```bash
curl -X DELETE "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters/DARK_MODE" \
  -H "X-User-Id: dev@local.dev"
```

### Listar usuários (apenas admin)

```bash
curl -X GET "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/users" \
  -H "X-User-Id: admin@local.dev"
```

### Criar novo usuário (apenas admin)

```bash
curl -X POST "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/users" \
  -H "X-User-Id: admin@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "novo.usuario@local.dev",
    "nome": "Novo Usuário",
    "permissoes": {
      "leitura": true,
      "escrita": false,
      "admin": false
    },
    "ativo": true
  }'
```

## 🔍 Interagir Diretamente com o Parameter Store

Você pode usar o AWS CLI apontando para o LocalStack:

```bash
# Instalar awslocal (facilita comandos)
pip install awscli-local

# Listar todos os parâmetros
awslocal ssm describe-parameters

# Obter valor de um parâmetro
awslocal ssm get-parameter --name "/feature-flags/flags/DARK_MODE"

# Listar parâmetros por caminho
awslocal ssm get-parameters-by-path --path "/feature-flags/flags/ui"
```

## 🧪 Testar a API Rapidamente

```bash
./test-api.sh
```

Este comando executa uma bateria de testes básicos:
- Lista parâmetros
- Obtém parâmetro específico
- Lista usuários

## 🐛 Debug

### Ver logs da Lambda

```bash
./logs-lambda.sh
```

### Ver logs do LocalStack

```bash
./logs.sh
```

### Recriar função Lambda

Se você fez alterações no código:

```bash
./restart.sh
```

## 📁 Estrutura do Projeto

```
.
├── docker-compose.yml          # Orquestração dos containers
├── Dockerfile                  # Imagem da Lambda
├── *.sh                        # Scripts de automação (bash)
├── init-localstack.sh          # Script de inicialização do LocalStack
├── .env.example                # Variáveis de ambiente exemplo
├── lambda_function.py          # Entry point da Lambda
├── requirements.txt            # Dependências Python
├── src/                        # Código fonte
│   ├── handler.py             # Handler principal
│   ├── router.py              # Roteamento de requisições
│   ├── controllers/           # Controllers (camada HTTP)
│   ├── services/              # Lógica de negócio
│   ├── repositories/          # Acesso a dados
│   ├── validators/            # Validações
│   └── middlewares/           # Middlewares (auth, etc)
└── tests/                      # Testes
```

## 🔧 Configuração Avançada

### Alterar região AWS

Edite o arquivo [.env.example](.env.example) e copie para `.env`:

```bash
cp .env.example .env
```

Altere a variável `AWS_REGION` conforme necessário.

### Persistência de Dados

Os dados do LocalStack são armazenados em `./localstack-data`. Para limpar tudo:

```bash
./clean.sh
```

## ⚠️ Limitações do Ambiente Local

- LocalStack simula os serviços AWS, mas pode ter diferenças de comportamento
- Performance pode ser diferente da AWS real
- Alguns recursos avançados podem não estar disponíveis
- Use apenas para desenvolvimento e testes

## 📚 Documentação Adicional

- [Estrutura de Parâmetros](docs/PARAMETER_STRUCTURE.md)
- [Usuários e Permissões](docs/USERS_AND_PERMISSIONS.md)
- [Exemplos](docs/EXAMPLES.md)
- [Arquitetura](docs/ARCHITECTURE_DIAGRAM.md)

## 🆘 Troubleshooting

### Container não sobe

```bash
# Verificar logs
./logs.sh

# Recriar do zero
./clean.sh
./build.sh
./up.sh
```

### Erro de permissão no script

```bash
chmod +x *.sh
```

### Lambda não responde

```bash
# Ver logs da Lambda
./logs-lambda.sh

# Verificar se a função foi criada
awslocal lambda list-functions
```

### Porta 4566 já em uso

Pare outros containers LocalStack em execução:

```bash
docker ps | grep localstack
docker stop <container_id>
```

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.
