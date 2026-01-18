# 🌐 Swagger UI - Feature Flag Manager

## ✅ Implementação Completa

O projeto agora possui **Swagger UI totalmente funcional** acessível via browser!

## 🚀 Como Usar

### 1. Subir o Ambiente

```bash
./up.sh
```

### 2. Iniciar o Swagger UI

```bash
./swagger-ui.sh
```

### 3. Acessar no Browser

Abra: **http://localhost:8080/**

## 📊 O que Foi Implementado

### Arquivos Criados

1. **openapi.yaml** - Especificação OpenAPI 3.0 completa com todos os endpoints
2. **src/swagger_handler.py** - Handler Lambda que serve o Swagger UI
3. **swagger-proxy.py** - Servidor HTTP que converte requisições do browser em invocações Lambda
4. **swagger-ui.sh** - Script para iniciar o proxy
5. **test-swagger.sh** - Script de teste automatizado
6. **SWAGGER_GUIDE.md** - Guia completo de uso do Swagger UI

### Arquivos Modificados

1. **src/router.py** - Adicionadas rotas para /, /docs e /health
2. **requirements.txt** - Adicionado PyYAML
3. **docker-compose.yml** - Montados volumes com código fonte para Lambda
4. **init-localstack.sh** - Ajustado para criar Lambda via ZIP
5. **help.sh** - Adicionada seção Swagger UI
6. **LOCAL_DEVELOPMENT.md** - Adicionadas instruções do Swagger UI

## 🎯 Endpoints Disponíveis

### Interface Web
- `GET /` - Swagger UI (HTML interativo)
- `GET /docs` - Especificação OpenAPI (JSON)
- `GET /health` - Health check

### API Endpoints (todos testáveis pelo Swagger UI)

#### Parameters
- `GET /parameters` - Listar feature flags
- `POST /parameters` - Criar feature flag
- `GET /parameters/{id}` - Obter feature flag
- `PUT /parameters/{id}` - Atualizar feature flag
- `DELETE /parameters/{id}` - Deletar feature flag

#### Users  
- `GET /users` - Listar usuários
- `POST /users` - Criar usuário
- `GET /users/{id}` - Obter usuário
- `PUT /users/{id}` - Atualizar usuário
- `DELETE /users/{id}` - Deletar usuário

## 🔧 Como Funciona

```
Browser (localhost:8080)
    ↓ HTTP GET/POST
Swagger Proxy (Python HTTP Server)
    ↓ Lambda Invocation Event
LocalStack (Lambda Executor)
    ↓ Executa Lambda
Feature Flag Manager Lambda
    ↓ Retorna HTML (Swagger UI) ou JSON (API)
Browser
```

## ✨ Recursos

- ✅ Swagger UI com CDN (sem instalação adicional)
- ✅ Documentação completa de todos os endpoints
- ✅ Teste interativo direto do browser
- ✅ Header X-User-Id preenchido automaticamente
- ✅ Exemplos de requisições e respostas
- ✅ Validação de schemas
- ✅ Suporte completo a autenticação e permissões

## 📝 Testes Realizados

```bash
$ ./test-swagger.sh

🌐 Testando Swagger UI...

1️⃣  Testando /health...
{
  "status": "healthy",
  "service": "feature-flag-manager",
  "swagger_ui": "available at /"
}

2️⃣  Testando / (Swagger UI)...
Status: 200
Content-Type: text/html; charset=utf-8
Body length: 2879 caracteres
Contém Swagger UI: True

3️⃣  Testando /docs (OpenAPI Spec)...
OpenAPI Version: 3.0.0
Título: Feature Flag Manager API
Paths: 7 endpoints

✅ Testes concluídos!
```

## 🎓 Para Aprender Mais

- Leia o [SWAGGER_GUIDE.md](SWAGGER_GUIDE.md) para guia completo
- Execute `./help.sh` para ver todos os comandos
- Acesse o Swagger UI e explore a interface interativa

## 🙋 FAQ

**Q: Por que preciso do swagger-proxy.py?**
A: O LocalStack Lambda só aceita invocações POST com payload JSON. O proxy converte requisições HTTP normais (GET, POST, etc.) do browser em invocações Lambda.

**Q: Posso mudar a porta 8080?**
A: Sim! Edite a variável `port` no arquivo `swagger-proxy.py`.

**Q: O Swagger UI funciona em produção?**
A: Não, este setup é apenas para desenvolvimento local. Para produção, use API Gateway com integração Lambda.

**Q: Como paro o servidor?**
A: Pressione `Ctrl+C` no terminal onde o `swagger-ui.sh` está rodando.

## 🎉 Pronto!

Agora você pode acessar a aplicação localmente usando o Swagger no browser! 

Execute:
```bash
./swagger-ui.sh
```

E acesse: **http://localhost:8080/**
