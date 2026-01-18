# Scripts Bash - Feature Flag Manager

Scripts de automação para gerenciar o ambiente Docker LocalStack.

## 🚀 Como usar

Todos os scripts são executáveis no Git Bash (Windows), Bash (Linux) ou Terminal (Mac):

```bash
./nome-do-script.sh
```

## 📋 Scripts Disponíveis

### Build e Inicialização

- **`./build.sh`** - Builda as imagens Docker
- **`./up.sh`** - Sobe o ambiente completo (LocalStack + Lambda)
- **`./down.sh`** - Para o ambiente
- **`./restart.sh`** - Reinicia o ambiente (útil após mudanças no código)

### Logs e Debug

- **`./logs.sh`** - Mostra logs do LocalStack em tempo real
- **`./logs-lambda.sh`** - Mostra logs da função Lambda
- **`./info.sh`** - Mostra informações do ambiente (URL, usuários, etc)

### Testes

- **`./test-api.sh`** - Testa a API com curl (rápido)
- **`./test-python.sh`** - Executa suite completa de testes Python
- **`./test-complete.sh`** - Testa parameters e users (OK + erro)
- **`./validate.sh`** - Valida se o ambiente está configurado corretamente

### Utilitários

- **`./help.sh`** - Mostra esta lista de comandos
- **`./clean.sh`** - Remove tudo (containers, volumes, dados)

## 🎯 Fluxo de Uso Típico

### Primeira vez

```bash
# 1. Build das imagens
./build.sh

# 2. Subir ambiente
./up.sh

# 3. Testar
./test-api.sh
```

### Desenvolvimento Diário

```bash
# Ver informações
./info.sh

# Ver logs
./logs.sh
./logs-lambda.sh

# Após mudanças no código
./restart.sh

# Testar mudanças
./test-api.sh
```

### Limpeza

```bash
# Parar ambiente
./down.sh

# Ou remover tudo
./clean.sh
```

## ⚙️ Permissões

Se você receber erro de permissão, execute:

```bash
chmod +x *.sh
```

## 📚 Documentação

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Guia de 5 minutos
- **[LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)** - Guia completo
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Referência rápida

## 💡 Dicas

- Use `./help.sh` para ver todos os comandos
- Use `./info.sh` para obter a URL da Lambda
- Use `./validate.sh` para diagnosticar problemas
- Use `./logs-lambda.sh` para debug da Lambda

---

**Nota**: Se você preferir usar Make, o Makefile ainda está disponível como alternativa.
