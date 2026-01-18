# Guia de Resolução de Problemas - Swagger UI

## ❌ Problema: Network não é removida ao executar down.sh

### Sintoma
```bash
./down.sh
# Mostra: "Network lambda-feature-flag-manager_lambda-network Resource is still..."
```

### Causa
O LocalStack cria containers Lambda automaticamente que ficam órfãos após o `down.sh`.

### Solução
O script [down.sh](down.sh) foi atualizado para limpar automaticamente:
- Containers Lambda órfãos
- Network que ficou presa

Execute novamente:
```bash
./down.sh
```

Se ainda assim houver problemas, execute manualmente:
```bash
# Remover containers Lambda órfãos
docker ps -a --filter "name=feature-flag-localstack-lambda" --format "{{.ID}}" | xargs docker rm -f

# Remover network
docker network rm lambda-feature-flag-manager_lambda-network
```

---

## ❌ Problema: quickstart.sh detecta LocalStack rodando quando não está

### Sintoma
O script diz "✓ LocalStack já está rodando" mas o container não existe ou está parado.

### Causa
Verificação antiga não filtrava por status (containers parados eram detectados como rodando).

### Solução
O script [quickstart.sh](quickstart.sh) foi atualizado para verificar apenas containers **em execução**.

Execute novamente:
```bash
bash quickstart.sh
```

---

## ❌ Problema: Tela em branco ao acessar http://localhost:4566

### Causa
Você está tentando acessar a porta errada. O LocalStack (porta 4566) não serve HTML diretamente.

### Solução
✅ Acesse o Swagger UI em: **http://localhost:8080**

---

## ❌ Problema: "Failed to fetch" ou "CORS" no Swagger UI

### Causas Possíveis
1. A função Lambda não foi criada
2. O proxy do Swagger não está rodando
3. Os usuários não foram configurados

### Solução

```bash
# 1. Verificar se a Lambda existe
docker exec feature-flag-localstack awslocal lambda list-functions

# 2. Se não existir, executar:
bash run-init.sh

# 3. Verificar se o proxy está rodando
curl http://localhost:8080/health

# 4. Se não estiver, iniciar o proxy:
python swagger-proxy.py &
```

---

## ❌ Problema: Ambiente reiniciado (down.sh + up.sh) e nada funciona

### Causa
Após reiniciar o ambiente, a Lambda e os usuários precisam ser recriados.

### Solução

**Opção 1: Script automático (recomendado)**
```bash
bash quickstart.sh
```

**Opção 2: Manual**
```bash
# 1. Criar Lambda e usuários
bash run-init.sh

# 2. Iniciar proxy
python swagger-proxy.py &

# 3. Acessar http://localhost:8080
```

---

## ❌ Problema: "Permission denied" ao executar requisições

### Causa
Você está usando um usuário sem a permissão necessária.

### Solução

Verifique as permissões dos usuários:

| Usuário              | Permissões            | Pode fazer                    |
|----------------------|-----------------------|-------------------------------|
| admin@local.dev      | Admin                 | Tudo (criar/editar/deletar)   |
| dev@local.dev        | Leitura + Escrita     | Criar e editar flags          |
| analista@local.dev   | Apenas Leitura        | Apenas visualizar             |

Exemplo: Para criar um parâmetro, use `dev@local.dev` ou `admin@local.dev` no header `X-User-Id`.

---

## ✅ Checklist de Verificação

Antes de reportar um problema, verifique:

- [ ] LocalStack está rodando: `docker ps | grep localstack`
- [ ] Lambda existe: `docker exec feature-flag-localstack awslocal lambda list-functions`
- [ ] Usuários configurados: `curl -H "X-User-Id: admin@local.dev" http://localhost:8080/users`
- [ ] Proxy rodando: `curl http://localhost:8080/health`
- [ ] Acessando porta correta: **http://localhost:8080** (não 4566)

---

## 🔄 Reinicialização Completa

Se nada funcionar, reinicie tudo:

```bash
# 1. Parar tudo
./down.sh

# 2. Limpar volumes (opcional, apaga dados)
docker-compose down -v

# 3. Rebuildar
./build.sh

# 4. Iniciar tudo
bash quickstart.sh
```

---

## 📞 Comandos Úteis de Diagnóstico

```bash
# Ver logs do LocalStack
docker logs feature-flag-localstack -f

# Verificar saúde do ambiente
curl http://localhost:8080/health

# Listar usuários
curl -H "X-User-Id: admin@local.dev" http://localhost:8080/users

# Listar parâmetros
curl -H "X-User-Id: dev@local.dev" http://localhost:8080/parameters

# Verificar se Lambda está ativa
docker exec feature-flag-localstack awslocal lambda get-function --function-name feature-flag-manager
```
