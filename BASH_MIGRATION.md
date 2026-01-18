# ✅ Repositório Atualizado para Scripts Bash

O repositório foi completamente atualizado para usar **scripts bash** ao invés do Makefile, funcionando perfeitamente no Git Bash do Windows!

## 🎯 O que foi feito:

### ✅ 13 Scripts Bash Criados

1. **`./build.sh`** - Builda as imagens Docker
2. **`./up.sh`** - Sobe o ambiente (LocalStack + Lambda)
3. **`./down.sh`** - Para o ambiente
4. **`./restart.sh`** - Reinicia o ambiente
5. **`./logs.sh`** - Logs do LocalStack
6. **`./logs-lambda.sh`** - Logs da Lambda
7. **`./info.sh`** - Informações do ambiente
8. **`./clean.sh`** - Remove tudo
9. **`./test-api.sh`** - Testa a API (curl)
10. **`./test-python.sh`** - Testes Python completos
11. **`./help.sh`** - Lista todos os comandos
12. **`./validate.sh`** - Valida o ambiente (atualizado)
13. **`./init-localstack.sh`** - Script de inicialização (já existia)

### ✅ Documentação Atualizada

Todos os arquivos de documentação foram atualizados para usar os scripts bash:

- ✅ **LOCAL_DEVELOPMENT.md** - Guia completo atualizado
- ✅ **GETTING_STARTED.md** - Guia de 5 minutos atualizado
- ✅ **QUICK_REFERENCE.md** - Referência rápida atualizada
- ✅ **README.md** - Já estava atualizado
- ✅ **SCRIPTS_README.md** - Novo guia de scripts

### ✅ Permissões Configuradas

Todos os scripts foram tornados executáveis automaticamente:

```bash
chmod +x *.sh
```

## 🚀 Como Usar Agora

### Primeiro Uso

```bash
# 1. Build
./build.sh

# 2. Subir ambiente
./up.sh

# 3. Ver informações
./info.sh

# 4. Testar
./test-api.sh
```

### Ver Todos os Comandos

```bash
./help.sh
```

Saída:
```
===================================
Feature Flag Manager - Comandos
===================================

🚀 Build e Inicialização:
  ./build.sh         - Builda as imagens Docker
  ./up.sh            - Sobe o ambiente (LocalStack + Lambda)
  ./down.sh          - Para o ambiente
  ./restart.sh       - Reinicia o ambiente

📋 Logs e Debug:
  ./logs.sh          - Mostra logs do LocalStack
  ./logs-lambda.sh   - Mostra logs da Lambda
  ./info.sh          - Mostra informações do ambiente

🧪 Testes:
  ./test-api.sh      - Testa a API (curl)
  ./test-python.sh   - Testa a API (Python completo)
  ./validate.sh      - Valida o ambiente

🧹 Limpeza:
  ./clean.sh         - Remove tudo (containers, volumes, dados)

📚 Documentação:
  cat GETTING_STARTED.md    - Guia de 5 minutos
  cat QUICK_REFERENCE.md    - Referência rápida
  cat LOCAL_DEVELOPMENT.md  - Guia completo
===================================
```

## ✅ Vantagens dos Scripts Bash

✅ **Funciona nativamente no Git Bash (Windows)**
✅ **Não precisa instalar Make**
✅ **Compatível com Linux e Mac**
✅ **Scripts simples e fáceis de entender**
✅ **Fácil de customizar e extender**

## 📚 Documentação

### Comece por aqui:
1. **[GETTING_STARTED.md](GETTING_STARTED.md)** - Guia de 5 minutos
2. **[SCRIPTS_README.md](SCRIPTS_README.md)** - Guia dos scripts
3. **[LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)** - Guia completo

### Para desenvolvimento:
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Comandos rápidos
- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Setup e troubleshooting

## 🎯 Próximos Passos

Execute agora:

```bash
# Ver ajuda
./help.sh

# Buildar
./build.sh

# Subir ambiente
./up.sh
```

---

**Status**: ✅ Repositório 100% funcional com scripts bash no Git Bash do Windows!

**Última atualização**: Janeiro 2026
