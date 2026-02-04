# Feature Flag Manager API

Sistema de gerenciamento de feature flags com suporte a usuários e permissões, rodando completamente local com LocalStack.

## 🚀 Início Rápido - Ambiente Local

Este é um projeto de **prova de conceito** focado em desenvolvimento local usando Docker e LocalStack.

### Inicialização Automática (Recomendado)

```bash
# Inicialização completa em um comando
bash quickstart.sh
1. ✅ Verificar/iniciar o LocalStack
2. ✅ Criar a função Lambda
3. ✅ Configurar os três usuários (admin, dev, analista)
4. ✅ Iniciar o Swagger UI em http://localhost:8080

### Inicialização Manual (Passo a Passo)

```bash
# 1. Buildar as imagens
./build.sh

# 2. Subir o ambiente (LocalStack + Lambda + Parameter Store)
./up.sh

# 3. Inicializar a Lambda e usuários
bash run-init.sh

# 4. Iniciar o Swagger UI (em outro terminal ou use & no final)
bash start-swagger.sh

# 5. Acessar o Swagger UI
# Abra no navegador: http://localhost:8080
```

**⚠️ IMPORTANTE**: O Swagger UI está disponível em `http://localhost:8080` (não na porta 4566)

📖 **Documentação completa de desenvolvimento local**: [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)

## 📖 Swagger UI - Interface Web da API

Este projeto inclui uma interface web interativa (Swagger UI) para testar e documentar a API.

### Como Acessar

Após inicializar o ambiente:

```bash
# Opção 1: Script automático (recomendado)
bash start-swagger.sh

# Opção 2: Manual
python swagger-proxy.py
```

Então acesse no navegador: **http://localhost:8080**

**⚠️ Observação**: 
- O LocalStack roda na porta **4566** (apenas invocações Lambda diretas)
- O Swagger UI roda na porta **8080** (interface web amigável)
- Use sempre a porta **8080** para acessar via navegador

### Funcionalidades do Swagger UI

- ✅ Interface visual para testar todos os endpoints
- ✅ Documentação automática da API
- ✅ Header `X-User-Id` adicionado automaticamente
- ✅ Exemplos de requisições e respostas
- ✅ Validação de schemas em tempo real

### Pré-requisitos

- Docker e Docker Compose
- Git Bash (Windows) ou Bash (Linux/Mac)
- Python 3.11+ (opcional, para testes)

## ⚠️ Estrutura de Parâmetros

Este projeto utiliza uma estrutura JSON padronizada para todos os parâmetros feature flags:

📖 **Documentação completa**: [PARAMETER_STRUCTURE.md](docs/PARAMETER_STRUCTURE.md)

### Principais Características:
- ✅ **Metadados Completos**: ID, tipo, descrição, timestamp, usuário
- ✅ **Tipos Suportados**: BOOLEAN, STRING, INTEGER, DOUBLE, DATE, TIME, DATETIME, JSON
- ✅ **Histórico de Versão**: Rastreamento automático da versão anterior
- ✅ **Auditoria**: Rastreamento de modificações por usuário e timestamp
- 🔐 **Sistema de Permissões**: Controle de acesso baseado em roles (leitura, escrita, admin)
- 🏷️ **Prefixos Customizados**: Organize flags por domínio/módulo

### Estrutura de Armazenamento

- **Feature Flags**: `/feature-flags/flags/{prefix}/{id}`
- **Usuários**: `/feature-flags/users`

📖 **Sistema de Usuários e Permissões**: [USERS_AND_PERMISSIONS.md](docs/USERS_AND_PERMISSIONS.md)

## Arquitetura

Este projeto segue os **princípios SOLID** e padrões de clean architecture:

- **Single Responsibility Principle (SRP)**: Cada classe tem uma responsabilidade bem definida
- **Open/Closed Principle**: Código aberto para extensão, fechado para modificação
- **Liskov Substitution Principle**: Interfaces de repositório podem ser substituídas
- **Interface Segregation Principle**: Interfaces pequenas e focadas
- **Dependency Inversion Principle**: Módulos de alto nível dependem de abstrações

📂 **Ver estrutura completa**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

### Estrutura do Projeto

```
├── lambda_function.py           # AWS Lambda entry point
├── docker-compose.yml           # Orquestração LocalStack
├── Dockerfile                   # Imagem da Lambda
├── Makefile                     # Comandos de automação
├── init-localstack.sh          # Script de inicialização
├── src/
│   ├── handler.py              # API handler
│   ├── router.py               # Roteamento com autorização
│   ├── exceptions.py           # Exceções customizadas
│   ├── controllers/            # Camada HTTP
│   │   ├── parameter_controller.py
│   │   └── user_controller.py
│   ├── services/               # Lógica de negócio
│   │   ├── parameter_service.py
│   │   └── user_service.py
│   ├── repositories/           # Acesso a dados
│   │   ├── parameter_repository.py
│   │   └── user_repository.py
│   ├── validators/             # Validação de entrada
│   │   └── parameter_validator.py
│   └── middlewares/            # Middlewares
│       └── authorization.py
├── tests/                      # Testes
│   ├── events/                 # Eventos de teste
│   └── *.py                    # Unit tests
├── docs/                       # Documentação
│   ├── PARAMETER_STRUCTURE.md
│   ├── USERS_AND_PERMISSIONS.md
│   ├── EXAMPLES.md
│   └── ARCHITECTURE_DIAGRAM.md
└── requirements.txt            # Dependências Python
```

## 👥 Usuários Pré-configurados (Ambiente Local)

| Email                | Permissões | Descrição                  |
| -------------------- | ---------- | -------------------------- |
| `admin@local.dev`    | Admin      | Gerenciar usuários e flags |
| `dev@local.dev`      | Escrita    | Criar e alterar flags      |
| `analista@local.dev` | Leitura    | Apenas visualizar          |

## Funcionalidades

### 🔐 Sistema de Permissões

A API inclui um sistema completo de gerenciamento de usuários com controle de acesso baseado em roles:

- **leitura**: Visualizar parâmetros e usuários
- **escrita**: Criar e atualizar parâmetros  
- **admin**: Acesso completo incluindo gerenciamento de usuários

Todas as requisições devem incluir o header `X-User-Id` para autenticação.

📖 **Documentação completa**: [USERS_AND_PERMISSIONS.md](docs/USERS_AND_PERMISSIONS.md)

### 1. Listar Parâmetros
**Endpoint**: `GET /parameters`
**Permissão**: `leitura`

Lista todos os feature flags com o prefixo `/feature-flags/flags`, ordenados hierarquicamente por caminho.

**Exemplo**:
```bash
curl -X GET "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters" \
  -H "X-User-Id: dev@local.dev"
```

**Response**:
```json
{
  "parameters": [
    {
      "id": "API_RETRIES",
      "value": "3",
      "type": "INTEGER",
      "description": "Número de tentativas da API",
      "lastModifiedAt": "2026-01-18T02:40:07Z",
      "lastModifiedBy": "",
      "arn": "arn:aws:ssm:us-east-1:000000000000:parameter/feature-flags/flags/api/API_RETRIES"
    },
    {
      "id": "API_TIMEOUT",
      "value": "5000",
      "type": "INTEGER",
      "description": "Timeout da API em ms",
      "lastModifiedAt": "2026-01-18T02:39:59Z",
      "lastModifiedBy": "",
      "arn": "arn:aws:ssm:us-east-1:000000000000:parameter/feature-flags/flags/api/API_TIMEOUT"
    }
  ]
}
```

### 1.1 Listar Parâmetros por Prefixo
**Endpoint**: `GET /parameters/prefix/{prefix}`
**Permissão**: `leitura`

Lista apenas os feature flags que estão sob um prefixo específico (ex: `ui`, `api`, `config`).

**Exemplo**:
```bash
curl -X GET "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters/prefix/api" \
  -H "X-User-Id: dev@local.dev"
```

**Response**:
```json
{
  "prefix": "api",
  "parameters": [
    {
      "id": "API_RETRIES",
      "value": "3",
      "type": "INTEGER",
      "description": "Número de tentativas da API",
      "lastModifiedAt": "2026-01-18T02:40:07Z",
      "lastModifiedBy": "",
      "arn": "arn:aws:ssm:us-east-1:000000000000:parameter/feature-flags/flags/api/API_RETRIES",
      "prefix": "api"
    }
  ]
}
```

### 1.2 Listar Prefixos Disponíveis
**Endpoint**: `GET /parameters/prefixes`
**Permissão**: `leitura`

Retorna todos os prefixos únicos disponíveis sob `/feature-flags/flags/` (ex: `api`, `config`, `ui`).

**Exemplo**:
```bash
curl -X GET "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters/prefixes" \
  -H "X-User-Id: dev@local.dev"
```

**Response**:
```json
{
  "prefixes": ["api", "config"]
}
```

### 2. Criar Parâmetro
**Endpoint**: `POST /parameters`
**Permissão**: `admin`

Cria um novo feature flag com estrutura completa de metadados.

**Exemplo**:
```bash
curl -X POST "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters" \
  -H "X-User-Id: dev@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "MY_FEATURE",
    "value": "true",
    "type": "BOOLEAN",
    "description": "Controla minha feature",
    "lastModifiedBy": "dev@local.dev",
    "prefix": "ui"
  }'
```

**Nota**: O campo `prefix` é opcional. Se fornecido, o parâmetro será criado em `/feature-flags/flags/{prefix}/{id}`, caso contrário em `/feature-flags/flags/{id}`.

**Tipos suportados**: `BOOLEAN`, `STRING`, `INTEGER`, `DOUBLE`, `DATE`, `TIME`, `DATETIME`, `JSON`

**Response** (201 Created):
```json
{
  "message": "Parameter created successfully",
  "id": "MY_FEATURE",
  "parameter": {
    "id": "MY_FEATURE",
    "value": "true",
    "type": "BOOLEAN",
    "description": "Controla minha feature",
    "lastModifiedAt": "2026-01-14T10:00:00Z",
    "lastModifiedBy": "dev@local.dev"
  }
}
```

### 3. Atualizar Parâmetro
**Endpoint**: `PUT /parameters/{parameterId}`
**Permissão**: `escrita`

Atualiza um feature flag existente. Apenas `value` e `description` podem ser atualizados.

**Exemplo**:
```bash
curl -X PUT "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters/contingencia/CONTINGENCIA_TOTAL_ONLINE" \
  -H "X-User-Id: dev@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "value": "false",
    "description": "Descrição atualizada"
  }'
```

**Nota**: Se o parâmetro possui prefixo, use o formato `{prefix}/{id}` no path.

**Response** (200 OK):
```json
{
  "message": "Parameter updated successfully",
  "id": "MY_FEATURE"
}
```

### 4. Deletar Parâmetro
**Endpoint**: `DELETE /parameters/{parameterId}`
**Permissão**: `escrita`

**Exemplo**:
```bash
curl -X DELETE "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters/contingencia/CONTINGENCIA_TOTAL_ONLINE" \
  -H "X-User-Id: admin@local.dev"
```

### 5. Gerenciamento de Usuários

#### Listar Usuários
**Endpoint**: `GET /users`
**Permissão**: `leitura`

**Exemplo**:
```bash
curl -X GET "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/users" \
  -H "X-User-Id: admin@local.dev"
```

#### Criar Usuário
**Endpoint**: `POST /users`
**Permissão**: `admin`

**Exemplo**:
```bash
curl -X POST "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/users" \
  -H "X-User-Id: admin@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "usuario@exemplo.com",
    "nome": "Nome do Usuário",
    "permissoes": {
      "leitura": true,
      "escrita": true,
      "admin": false
    },
    "ativo": true
  }'
```

#### Atualizar Usuário
**Endpoint**: `PUT /users/{userId}`
**Permissão**: `admin`

Atualiza um usuário existente. O campo `id` não pode ser alterado.

**Exemplo**:
```bash
curl -X PUT "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/users/dev%40local.dev" \
  -H "X-User-Id: admin@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Novo Nome",
    "permissoes": {
      "leitura": true,
      "escrita": true,
      "admin": false
    },
    "ativo": true
  }'
```

#### Deletar Usuário
**Endpoint**: `DELETE /users/{userId}`
**Permissão**: `admin`

📖 **Documentação completa da API de usuários**: [USERS_AND_PERMISSIONS.md](docs/USERS_AND_PERMISSIONS.md)

## 📚 Documentação Completa

- **[LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)** - Guia completo do ambiente local
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Resolução de problemas comuns
- **[PARAMETER_STRUCTURE.md](docs/PARAMETER_STRUCTURE.md)** - Estrutura JSON dos parâmetros
- **[USERS_AND_PERMISSIONS.md](docs/USERS_AND_PERMISSIONS.md)** - Sistema de usuários e permissões
- **[EXAMPLES.md](docs/EXAMPLES.md)** - Exemplos práticos de uso
- **[ARCHITECTURE_DIAGRAM.md](docs/ARCHITECTURE_DIAGRAM.md)** - Diagramas de arquitetura

## 🧪 Testes

Eventos de teste disponíveis em [`tests/events/`](tests/events/) para testes locais.

Para executar testes rápidos no ambiente local:

```bash
make test-api
```

## 🔍 Comandos Úteis

```bash
# Ver logs em tempo real
make logs
make logs-lambda

# Reiniciar ambiente
make restart

# Parar ambiente (preserva dados)
./down.sh

# Limpeza completa (remove volumes e dados)
bash clean-all.sh

# Informações do ambiente
make info

# Inicialização rápida completa
bash quickstart.sh
```

### Scripts Disponíveis

| Script | Descrição |
|--------|-----------|
| `quickstart.sh` | Inicialização automática completa (recomendado) |
| `build.sh` | Constrói as imagens Docker |
| `up.sh` | Sobe o ambiente LocalStack |
| `down.sh` | Para o ambiente e limpa containers órfãos |
| `run-init.sh` | Inicializa Lambda e usuários |
| `start-swagger.sh` | Inicia apenas o Swagger UI |
| `clean-all.sh` | Limpeza completa (remove dados) |

## ⚡ Boas Práticas Implementadas

1. **Separation of Concerns**: Controllers, services, repositories claramente separados
2. **Dependency Injection**: Dependências injetadas via construtores
3. **Error Handling**: Exceções customizadas com propagação adequada
4. **Logging**: Logging estruturado em toda aplicação
5. **Validation**: Validação de entrada antes do processamento
6. **Type Hints**: Anotações de tipo completas
7. **Documentation**: Docstrings abrangentes

## 📄 Licença

Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🚧 Roadmap (Produção)

Este é um projeto de **prova de conceito**. Para ir para produção, será necessário:

- [ ] Implementar testes unitários e de integração completos
- [ ] Configurar CI/CD pipeline
- [ ] Criar infraestrutura como código (Terraform/CloudFormation)
- [ ] Implementar API Gateway com autenticação real (Cognito/OAuth)
- [ ] Adicionar métricas e observabilidade (CloudWatch, X-Ray)
- [ ] Implementar rate limiting e throttling
- [ ] Documentar processo de deploy para produção
- [ ] Implementar backup e disaster recovery
- [ ] Adicionar conformidade e auditoria
