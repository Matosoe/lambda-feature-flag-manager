# Feature Flag Manager API

Sistema de gerenciamento de feature flags com suporte a usuários e permissões, rodando completamente local com LocalStack.

## 🚀 Início Rápido - Ambiente Local

Este é um projeto de **prova de conceito** focado em desenvolvimento local usando Docker e LocalStack.

```bash
# 1. Buildar as imagens
./build.sh

# 2. Subir o ambiente (LocalStack + Lambda + Parameter Store)
./up.sh

# 3. Testar a API
./test-api.sh
```

📖 **Documentação completa de desenvolvimento local**: [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)

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

Lista todos os feature flags com o prefixo `/feature-flags/flags`.

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
      "id": "DARK_MODE",
      "value": "true",
      "type": "BOOLEAN",
      "description": "Habilita modo escuro",
      "lastModifiedAt": "2026-01-14T10:00:00Z",
      "lastModifiedBy": "admin@local.dev"
    }
  ]
}
```

### 2. Criar Parâmetro
**Endpoint**: `POST /parameters`
**Permissão**: `escrita`

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

Atualiza um feature flag existente. Todos os campos são opcionais.

**Exemplo**:
```bash
curl -X PUT "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters/MY_FEATURE" \
  -H "X-User-Id: dev@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "value": "false",
    "description": "Descrição atualizada",
    "lastModifiedBy": "dev@local.dev",
    "prefix": "ui"
  }'
```

**Nota**: Se o parâmetro foi criado com um prefixo, você deve fornecer o mesmo prefixo ao atualizar.

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
curl -X DELETE "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations/parameters/MY_FEATURE" \
  -H "X-User-Id: dev@local.dev"
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

#### Deletar Usuário
**Endpoint**: `DELETE /users/{userId}`
**Permissão**: `admin`

📖 **Documentação completa da API de usuários**: [USERS_AND_PERMISSIONS.md](docs/USERS_AND_PERMISSIONS.md)

## 📚 Documentação Completa

- **[LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)** - Guia completo do ambiente local
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

# Limpar tudo (dados, containers, volumes)
make clean

# Informações do ambiente
make info
```

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
