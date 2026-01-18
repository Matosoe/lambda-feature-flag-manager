# 🚀 Primeiros Passos - 5 Minutos

## 1️⃣ Subir o Ambiente (2 minutos)

```bash
./build.sh
./up.sh
```

Aguarde a mensagem de conclusão. O ambiente criará automaticamente:
- ✅ Lambda function
- ✅ 3 usuários (admin, dev, analista)
- ✅ 4 feature flags de exemplo

## 2️⃣ Testar (1 minuto)

```bash
./test-api.sh
```

Você verá:
- Lista de parâmetros
- Detalhes do DARK_MODE
- Lista de usuários

## 3️⃣ Fazer sua Primeira Chamada (1 minuto)

```bash
# Obter a URL (será exibida após ./up.sh)
./info.sh

# Copie a Lambda Function URL e use:
curl -X GET "SUA_URL_AQUI/parameters" \
  -H "X-User-Id: dev@local.dev"
```

## 4️⃣ Criar sua Primeira Feature Flag (1 minuto)

```bash
curl -X POST "SUA_URL_AQUI/parameters" \
  -H "X-User-Id: dev@local.dev" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "MINHA_FEATURE",
    "value": "true",
    "type": "BOOLEAN",
    "description": "Minha primeira feature",
    "lastModifiedBy": "dev@local.dev"
  }'
```

## ✅ Pronto!

Agora você pode:
- 📖 Ler a [documentação completa](LOCAL_DEVELOPMENT.md)
- 🧪 Executar `./test-python.sh` para testes completos
- 🔍 Ver logs com `./logs.sh` ou `./logs-lambda.sh`
- 📚 Consultar [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## Comandos Essenciais

```bash
./help.sh        # Ver todos os comandos
./info.sh        # Informações do ambiente
./restart.sh     # Reiniciar após mudanças no código
./down.sh        # Parar ambiente
./clean.sh       # Limpar tudo
```

---

## Troubleshooting Rápido

**Ambiente não sobe?**
```bash
./clean.sh
./build.sh
./up.sh
```

**Lambda não responde?**
```bash
./logs-lambda.sh
```

**Porta 4566 em uso?**
```bash
docker ps | grep localstack
docker stop <container_id>
make up
```

---

**💡 Dica**: Execute `./info.sh` a qualquer momento para ver a URL da Lambda e os usuários disponíveis.
