# Plano de reconstrução do repositório

## 1. Limpeza do Repositório
- Remover todos os arquivos e pastas, exceto:
  - PLAN.md (este plano)
  - README.md (instruções gerais)
  - .gitignore

## 2. Infraestrutura Local
- Criar infra/local/ com:
  - docker-compose.yml (serviços: localstack, ory/fake-oauth2-server)
  - up.sh, down.sh (scripts para subir/descer ambiente)
  - README.md (instruções de uso)

## 3. Site Estático SSO
- Criar web/ com:
  - index.html (HTML+JS puro)
  - sso.js (lógica OIDC fake, armazenamento de credenciais)
  - README.md (como rodar local e deploy S3)
  - deploy.sh (automatizar deploy no S3)

## 4. Lambda + Swagger UI
- Criar lambda/ com:
  - lambda_function.py (CRUD de parâmetros, autenticação via header)
  - requirements.txt
  - swagger/
    - openapi.yaml (contrato atual, adaptado para credenciais no header)
    - swagger-ui/ (cópia do Swagger UI)
  - README.md (como rodar/testar local e deploy)
  - deploy.sh (automatizar deploy Lambda e Swagger UI no S3)

## 5. Automatização de Deploy
- Scripts de deploy para:
  - web/ (site estático no S3)
  - lambda/ (deploy Lambda e upload Swagger UI no S3)
- Instruções no README.md principal

---

# Observações
- O openapi.yaml será o atual, apenas trocando o e-mail por credenciais no header.
- O CRUD da Lambda será mantido conforme está hoje.
- O SSO será simulado apenas localmente, sem claims/roles avançados.
- O site será HTML+JS puro.
- Todo deploy será automatizado via scripts.
- A Lambda só exporá endpoints, sem acessar arquivos do S3.
