# 🔄 Guia de Migração - Nova Estrutura de Pastas

## 📋 Resumo das Mudanças

O projeto foi reorganizado para melhor manutenibilidade e profissionalismo. Todos os arquivos foram movidos para pastas apropriadas.

## 🗺️ Mapa de Migração

### Arquivos de Documentação (Movidos para `docs/`)

| Localização Antiga | Localização Nova |
|-------------------|------------------|
| `PARAMETER_STRUCTURE.md` | `docs/PARAMETER_STRUCTURE.md` |
| `EXAMPLES.md` | `docs/EXAMPLES.md` |
| `ARCHITECTURE_DIAGRAM.md` | `docs/ARCHITECTURE_DIAGRAM.md` |
| `QUICKSTART_v2.md` | `docs/QUICKSTART_v2.md` |
| `PROJECT_SUMMARY.md` | `docs/PROJECT_SUMMARY.md` |

### Arquivos de Teste (Movidos para `tests/events/`)

| Localização Antiga | Localização Nova |
|-------------------|------------------|
| `test_event_create.json` | `tests/events/test_event_create.json` |
| `test_event_update.json` | `tests/events/test_event_update.json` |
| `test_event_list.json` | `tests/events/test_event_list.json` |
| `test_event_create_integer.json` | `tests/events/test_event_create_integer.json` |
| `test_event_create_double.json` | `tests/events/test_event_create_double.json` |
| `test_event_create_json.json` | `tests/events/test_event_create_json.json` |
| `test_event_create_date.json` | `tests/events/test_event_create_date.json` |

### Arquivos de Infraestrutura (Movidos para `infra/`)

| Localização Antiga | Localização Nova |
|-------------------|------------------|
| `openapi.yaml` | `infra/openapi.yaml` |
| `deploy.sh` | `infra/deploy.sh` |
| `Makefile` | `infra/Makefile` |

### Arquivos que Permaneceram na Raiz

- ✅ `README.md` - Documentação principal
- ✅ `LICENSE` - Licença do projeto
- ✅ `lambda_function.py` - Entry point
- ✅ `requirements.txt` - Dependências
- ✅ `requirements-dev.txt` - Dependências de dev
- ✅ `pyproject.toml` - Configuração Python
- ✅ `.gitignore` - Arquivos ignorados
- ✅ `src/` - Código fonte
- ✅ `tests/` - Testes (agora organizado)

### Novos Arquivos Criados

| Arquivo | Descrição |
|---------|-----------|
| `PROJECT_STRUCTURE.md` | Documentação visual da estrutura |
| `docs/README.md` | Índice da documentação |
| `tests/README.md` | Guia de testes |
| `infra/README.md` | Guia de deploy e infraestrutura |
| `MIGRATION_GUIDE.md` | Este arquivo |

## 🔧 Como Atualizar Seus Scripts

### Se você tinha scripts que referenciam arquivos antigos:

#### Exemplo 1: Executar testes
```bash
# ❌ Antes
python test_with_event.py test_event_create.json

# ✅ Agora
python test_with_event.py tests/events/test_event_create.json
```

#### Exemplo 2: Deploy
```bash
# ❌ Antes
./deploy.sh

# ✅ Agora
./infra/deploy.sh
# ou execute da raiz:
cd infra && ./deploy.sh
```

#### Exemplo 3: Referências em código
```python
# ❌ Antes
with open('test_event_create.json') as f:
    event = json.load(f)

# ✅ Agora
with open('tests/events/test_event_create.json') as f:
    event = json.load(f)
```

#### Exemplo 4: Links em Markdown
```markdown
<!-- ❌ Antes -->
Veja [EXAMPLES.md](EXAMPLES.md)

<!-- ✅ Agora -->
Veja [EXAMPLES.md](docs/EXAMPLES.md)
```

## 📝 Checklist de Migração

Se você tem um fork ou clone local:

- [ ] Fazer pull das mudanças
- [ ] Atualizar scripts de teste para usar `tests/events/`
- [ ] Atualizar scripts de deploy para usar `infra/`
- [ ] Atualizar links em documentação customizada
- [ ] Verificar se CI/CD precisa de ajustes
- [ ] Testar localmente antes de fazer deploy

## 🚀 Impacto em CI/CD

### GitHub Actions
```yaml
# Se você tinha:
- name: Test
  run: python test.py test_event_create.json

# Mude para:
- name: Test
  run: python test.py tests/events/test_event_create.json
```

### AWS CodeBuild
```yaml
# buildspec.yml
# Se você tinha referências aos arquivos antigos, atualize os caminhos
phases:
  build:
    commands:
      - ./infra/deploy.sh  # não mais ./deploy.sh
```

## 🔍 Verificar Mudanças Necessárias

Execute este comando para encontrar referências aos caminhos antigos:

```bash
# Buscar referências a test_event na raiz
grep -r "test_event[^/]" --include="*.py" --include="*.sh" --include="*.md" .

# Buscar referências a deploy.sh na raiz
grep -r "^\./deploy\.sh\|^deploy\.sh" --include="*.py" --include="*.sh" --include="*.md" .

# Buscar referências a openapi.yaml na raiz
grep -r "^openapi\.yaml\|^\./openapi\.yaml" --include="*.py" --include="*.sh" --include="*.md" .
```

## 💡 Benefícios da Nova Estrutura

1. **Organização Clara**
   - Documentação toda em um lugar
   - Testes organizados
   - Infra separada

2. **Navegação Fácil**
   - Cada pasta tem README
   - Links funcionam corretamente
   - Estrutura intuitiva

3. **Profissional**
   - Segue padrões da indústria
   - Facilita onboarding
   - Melhor para open source

4. **Manutenível**
   - Fácil adicionar novos arquivos
   - Separação de responsabilidades
   - Escalável

## 🆘 Problemas Comuns

### Erro: "File not found: test_event_create.json"
**Solução**: Atualize o caminho para `tests/events/test_event_create.json`

### Erro: "deploy.sh: command not found"
**Solução**: Use `./infra/deploy.sh` ou `cd infra && ./deploy.sh`

### Links quebrados na documentação
**Solução**: Os links já foram atualizados. Faça pull das mudanças.

### Scripts de CI/CD falhando
**Solução**: Atualize os caminhos nos arquivos de configuração (`.github/workflows/`, `buildspec.yml`, etc.)

## 📞 Suporte

Se você encontrar problemas após a migração:

1. Verifique o [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) para a estrutura atualizada
2. Consulte os READMEs em cada pasta
3. Use a busca do editor para encontrar arquivos
4. Verifique este guia de migração

## ✅ Validação Pós-Migração

Execute estes comandos para validar que tudo está funcionando:

```bash
# 1. Verificar estrutura
ls -la docs/ tests/events/ infra/

# 2. Testar localmente
python -c "from lambda_function import lambda_handler; import json; print('✅ Import OK')"

# 3. Executar testes (se tiver pytest)
pytest tests/

# 4. Verificar se deploy.sh existe
test -f infra/deploy.sh && echo "✅ deploy.sh encontrado"

# 5. Verificar se openapi.yaml existe
test -f infra/openapi.yaml && echo "✅ openapi.yaml encontrado"
```

## 📚 Documentação Relacionada

- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Estrutura completa
- [README.md](README.md) - Documentação principal
- [docs/README.md](docs/README.md) - Índice de documentação
- [tests/README.md](tests/README.md) - Guia de testes
- [infra/README.md](infra/README.md) - Guia de deploy

---

✨ **A migração está completa!** Todos os arquivos foram organizados e a documentação atualizada.
