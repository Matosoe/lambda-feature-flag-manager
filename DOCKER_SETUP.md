# 🐳 Ambiente Docker LocalStack - Feature Flag Manager

## ✅ O que foi criado

Este ambiente Docker completo permite desenvolver e testar localmente todas as funcionalidades do Feature Flag Manager sem precisar de uma conta AWS.

### Arquivos criados:

1. **docker-compose.yml** - Orquestração do LocalStack e Lambda
2. **Dockerfile** - Imagem da Lambda function
3. **init-localstack.sh** - Script que inicializa automaticamente:
   - Lambda function
   - 3 usuários (admin, dev, analista)
   - 4 feature flags de exemplo
4. **Makefile** - Comandos para gerenciar o ambiente
5. **test_local_environment.py** - Suite de testes automatizados
6. **LOCAL_DEVELOPMENT.md** - Documentação completa
7. **QUICK_REFERENCE.md** - Referência rápida
8. **.env.example** - Variáveis de ambiente

### Arquivos removidos (não necessários para POC):

- ❌ `infra/` - Infraestrutura AWS removida
- ❌ `scripts/` - Scripts de produção removidos

## 🚀 Como usar

### 1. Primeira vez

```bash
# Build das imagens Docker
make build

# Subir o ambiente (aguarda 30s para inicialização)
make up
```

Após o `make up`, o ambiente estará pronto com:
- ✅ LocalStack rodando na porta 4566
- ✅ Lambda function criada e acessível
- ✅ 3 usuários configurados
- ✅ 4 feature flags de exemplo

### 2. Testar a API

Duas opções:

**Opção A - Testes rápidos com curl:**
```bash
make test-api
```

**Opção B - Suite completa de testes Python:**
```bash
make install-dev    # Primeira vez apenas
make test-python
```

### 3. Comandos do dia a dia

```bash
make info          # Ver informações do ambiente
make logs          # Ver logs do LocalStack
make logs-lambda   # Ver logs da Lambda
make restart       # Reiniciar tudo
make down          # Parar ambiente
make clean         # Limpar tudo (dados, containers, volumes)
```

## 👥 Usuários Pré-configurados

O ambiente já vem com 3 usuários prontos para uso:

| Email                | Permissões        | O que pode fazer                  |
| -------------------- | ----------------- | --------------------------------- |
| `admin@local.dev`    | Admin             | Tudo (gerenciar usuários e flags) |
| `dev@local.dev`      | Leitura + Escrita | Criar e alterar flags             |
| `analista@local.dev` | Apenas Leitura    | Apenas visualizar                 |

## 🚩 Feature Flags Pré-criadas

1. `/feature-flags/flags/ui/DARK_MODE` - Boolean
2. `/feature-flags/flags/api/MAX_RETRY` - Integer
3. `/feature-flags/flags/config/API_TIMEOUT` - Double
4. `/feature-flags/flags/MAINTENANCE_MODE` - Boolean (sem prefixo)

## 📝 Exemplo de uso

```bash
# Obter a URL da função Lambda (será exibida após make up)
# Exemplo: http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations

# Listar todos os parâmetros
curl -X GET "http://localhost:4566/.../parameters" \
  -H "X-User-Id: dev@local.dev"

# Criar novo parâmetro com prefixo
curl -X POST "http://localhost:4566/.../parameters" \
  -H "X-User-Id: dev@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "NOVA_FEATURE",
    "value": "true",
    "type": "BOOLEAN",
    "description": "Minha nova feature",
    "prefix": "mobile",
    "lastModifiedBy": "dev@local.dev"
  }'

# Atualizar parâmetro
curl -X PUT "http://localhost:4566/.../parameters/NOVA_FEATURE" \
  -H "X-User-Id: dev@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "value": "false",
    "description": "Feature desabilitada",
    "prefix": "mobile",
    "lastModifiedBy": "dev@local.dev"
  }'

# Deletar parâmetro
curl -X DELETE "http://localhost:4566/.../parameters/NOVA_FEATURE" \
  -H "X-User-Id: dev@local.dev"

# Listar usuários (requer permissão admin)
curl -X GET "http://localhost:4566/.../users" \
  -H "X-User-Id: admin@local.dev"
```

## 🧪 Testes Automatizados

O script `test_local_environment.py` executa uma bateria completa de testes:

1. ✅ Listar parâmetros
2. ✅ Obter parâmetro específico
3. ✅ Criar parâmetro
4. ✅ Atualizar parâmetro
5. ✅ Deletar parâmetro
6. ✅ Listar usuários
7. ✅ Validar permissões (tenta criar com usuário sem permissão)

Execute com:
```bash
make test-python
```

## 🔧 Estrutura do Ambiente

```
LocalStack Container
├── Lambda Service (porta 4566)
│   └── feature-flag-manager function
│       └── Function URL gerada automaticamente
│
└── SSM Parameter Store
    ├── /feature-flags/users
    │   └── JSON com array de usuários
    │
    └── /feature-flags/flags/
        ├── ui/
        │   └── DARK_MODE
        ├── api/
        │   └── MAX_RETRY
        ├── config/
        │   └── API_TIMEOUT
        └── MAINTENANCE_MODE
```

## 🐛 Troubleshooting

### LocalStack não sobe

```bash
# Ver logs
make logs

# Tentar limpar e recriar
make clean
make build
make up
```

### Lambda não responde

```bash
# Ver logs da Lambda
make logs-lambda

# Verificar se a função existe
awslocal lambda list-functions

# Recriar função
make restart
```

### Porta 4566 já em uso

```bash
# Encontrar e parar outros containers LocalStack
docker ps | grep localstack
docker stop <container_id>

# Ou parar todos
docker stop $(docker ps -q --filter ancestor=localstack/localstack)
```

### Erro de permissão no init script

```bash
chmod +x init-localstack.sh
make restart
```

## 📚 Documentação Completa

- **[LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)** - Guia completo e detalhado
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Referência rápida de comandos
- **[README.md](README.md)** - Documentação principal do projeto
- **[USERS_AND_PERMISSIONS.md](docs/USERS_AND_PERMISSIONS.md)** - Sistema de permissões
- **[PARAMETER_STRUCTURE.md](docs/PARAMETER_STRUCTURE.md)** - Estrutura dos parâmetros

## 💡 Dicas

1. **Persistência**: Os dados ficam em `./localstack-data`. Use `make clean` para limpar tudo.

2. **AWS CLI Local**: Instale o `awslocal` para facilitar comandos:
   ```bash
   make install-aws-cli
   awslocal ssm get-parameter --name /feature-flags/flags/DARK_MODE
   ```

3. **Development Workflow**:
   - Faça alterações no código
   - Execute `make restart` para recriar a Lambda
   - Use `make test-python` para validar

4. **Debug**: Use `make logs-lambda` para ver outputs de print/logging

## 🎯 Próximos Passos

Para evoluir de POC para produção:

1. Implementar testes unitários completos
2. Adicionar CI/CD pipeline
3. Criar infraestrutura como código (Terraform)
4. Implementar API Gateway com autenticação real
5. Adicionar observabilidade (CloudWatch, X-Ray)
6. Implementar rate limiting
7. Documentar processo de deploy

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs: `make logs` ou `make logs-lambda`
2. Tente reiniciar: `make restart`
3. Se persistir, limpe tudo: `make clean && make build && make up`

---

**🎉 Ambiente pronto para desenvolvimento!**

Execute `make help` para ver todos os comandos disponíveis.
