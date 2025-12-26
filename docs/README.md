# 📚 Documentação - Feature Flag Manager

Esta pasta contém toda a documentação detalhada do projeto.

## 📄 Índice de Documentos

### 🚀 Começando

- **[QUICKSTART_v2.md](QUICKSTART_v2.md)** - Guia rápido de início
  - Como criar sua primeira flag
  - Exemplos básicos de uso
  - Troubleshooting rápido

### 📖 Especificações

- **[PARAMETER_STRUCTURE.md](PARAMETER_STRUCTURE.md)** - Estrutura completa dos parâmetros
  - Descrição detalhada de cada campo
  - Tipos de valores suportados
  - Validações implementadas
  - Retrocompatibilidade

### 💻 Exemplos Práticos

- **[EXAMPLES.md](EXAMPLES.md)** - Exemplos de uso real
  - Exemplos para cada tipo de valor
  - Código Python para integração
  - Casos de uso por domínio
  - Exemplos de requisições cURL

### 🏗️ Arquitetura

- **[ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)** - Diagramas e arquitetura
  - Diagrama visual da estrutura JSON
  - Fluxo de dados completo
  - Validação de tipos
  - Casos de uso por domínio
  - Ciclo de vida de uma flag

### 📊 Visão Geral

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Resumo do projeto
  - Visão geral da arquitetura
  - Princípios SOLID aplicados
  - Estrutura de arquivos
  - Features implementadas

## 🔗 Links Úteis

- [← Voltar para o README principal](../README.md)
- [Ver especificação OpenAPI](../infra/openapi.yaml)
- [Ver eventos de teste](../tests/events/)

## 📋 Mapa de Navegação

```
lambda-feature-flag-manager/
├── README.md                          # Início - Leia primeiro
├── docs/                              # Você está aqui
│   ├── README.md                      # Este arquivo
│   ├── QUICKSTART_v2.md              # 🚀 Comece aqui se é novo
│   ├── PARAMETER_STRUCTURE.md        # 📖 Entenda a estrutura
│   ├── EXAMPLES.md                   # 💻 Exemplos práticos
│   ├── ARCHITECTURE_DIAGRAM.md       # 🏗️ Arquitetura visual
│   └── PROJECT_SUMMARY.md            # 📊 Visão completa
├── infra/                            # Scripts e configurações
│   ├── openapi.yaml                  # Especificação da API
│   ├── deploy.sh                     # Script de deploy
│   └── Makefile                      # Automação
├── tests/events/                     # Eventos de teste
│   ├── test_event_create.json        # Exemplo: criar flag
│   ├── test_event_update.json        # Exemplo: atualizar flag
│   └── ...                           # Mais exemplos
└── src/                              # Código fonte
    ├── controllers/
    ├── services/
    ├── repositories/
    └── validators/
```

## 🎯 Guia de Leitura Sugerido

### Para Iniciantes
1. [README.md](../README.md) - Visão geral do projeto
2. [QUICKSTART_v2.md](QUICKSTART_v2.md) - Comece a usar rapidamente
3. [EXAMPLES.md](EXAMPLES.md) - Veja exemplos práticos

### Para Desenvolvedores
1. [PARAMETER_STRUCTURE.md](PARAMETER_STRUCTURE.md) - Entenda a estrutura
2. [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) - Visualize a arquitetura
3. [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Detalhes técnicos

### Para DevOps
1. [../infra/deploy.sh](../infra/deploy.sh) - Script de deployment
2. [../infra/openapi.yaml](../infra/openapi.yaml) - Especificação da API
3. [EXAMPLES.md](EXAMPLES.md) - Exemplos de integração

## 💡 Dicas

- Use `Ctrl+F` ou `Cmd+F` para buscar tópicos específicos
- Todos os exemplos de código são testados e funcionais
- Links entre documentos funcionam no GitHub e editores Markdown
- Arquivos de teste em `tests/events/` podem ser usados diretamente

## 📝 Contribuindo para a Documentação

Se você encontrar algum erro ou quiser melhorar a documentação:
1. Edite o arquivo correspondente
2. Mantenha o formato Markdown consistente
3. Adicione exemplos quando apropriado
4. Atualize este índice se adicionar novos arquivos
