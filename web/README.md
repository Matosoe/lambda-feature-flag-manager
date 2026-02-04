# Web - Site Estático SSO

Site estático em HTML/JavaScript puro para autenticação via Microsoft SSO (Azure AD) e visualização de credenciais.

## Funcionalidades

- ✅ Autenticação SSO com Microsoft (Azure AD)
- ✅ Exibição de dados do usuário autenticado
- ✅ Visualização do Access Token
- ✅ Armazenamento de dados no localStorage
- ✅ Interface responsiva e moderna
- ✅ Modo demonstração (sem necessidade de configuração inicial)

## Modo Demonstração

O site funciona em modo demonstração por padrão, sem necessidade de configurar Azure AD. Para usar SSO real, siga as instruções na seção "Configuração SSO Real".

## Executar Localmente

### Opção 1: Servidor HTTP simples com Python

```bash
# Python 3
python -m http.server 8000

# ou Python 2
python -m SimpleHTTPServer 8000
```

Acesse: http://localhost:8000

### Opção 2: Servidor HTTP com Node.js

```bash
npx http-server -p 8000
```

Acesse: http://localhost:8000

### Opção 3: Visual Studio Code Live Server

1. Instale a extensão "Live Server"
2. Clique com o botão direito em `index.html`
3. Selecione "Open with Live Server"

## Configuração SSO Real (Azure AD)

### 1. Registrar aplicação no Azure AD

1. Acesse o [Portal Azure](https://portal.azure.com)
2. Navegue para **Azure Active Directory** > **App registrations** > **New registration**
3. Configure:
   - **Name**: Feature Flag Manager Web
   - **Supported account types**: Accounts in any organizational directory
   - **Redirect URI**: 
     - Type: Single-page application (SPA)
     - URL: `http://localhost:8000` (para local) e `https://seu-dominio.s3.amazonaws.com` (para produção)
4. Clique em **Register**

### 2. Configurar a aplicação

1. Na página da aplicação registrada, copie o **Application (client) ID**
2. Em **Authentication**:
   - Marque **Access tokens** e **ID tokens**
   - Adicione os URIs de redirecionamento necessários
3. Em **API permissions**:
   - Adicione: `User.Read`, `openid`, `profile`, `email`
   - Grant admin consent (se necessário)

### 3. Atualizar o código

1. Edite o arquivo `sso.js`
2. Substitua `YOUR_CLIENT_ID` pelo Client ID copiado:

```javascript
const msalConfig = {
    auth: {
        clientId: "SEU_CLIENT_ID_AQUI",
        authority: "https://login.microsoftonline.com/common",
        redirectUri: window.location.origin
    },
    // ...
};
```

3. No arquivo `index.html`, adicione a biblioteca MSAL antes do `sso.js`:

```html
<script src="https://alcdn.msauth.net/browser/2.30.0/js/msal-browser.min.js"></script>
<script src="sso.js"></script>
```

4. No arquivo `sso.js`, descomente a linha de inicialização:

```javascript
// Inicializar ao carregar a página
window.addEventListener('DOMContentLoaded', () => {
    initializeMsal(); // Descomente esta linha
    // checkLocalStorage(); // Comente esta linha
});
```

## Deploy no S3

### Pré-requisitos

- AWS CLI configurado
- Bucket S3 criado
- Permissões para upload no S3

### Deploy Manual

```bash
# Criar bucket (se não existir)
aws s3 mb s3://feature-flag-web

# Configurar bucket para hospedagem estática
aws s3 website s3://feature-flag-web --index-document index.html

# Upload dos arquivos
aws s3 sync . s3://feature-flag-web --exclude ".git/*" --exclude "*.sh" --exclude "README.md"

# Tornar arquivos públicos
aws s3 cp s3://feature-flag-web s3://feature-flag-web --recursive --acl public-read
```

### Deploy Automatizado

```bash
./deploy.sh
```

O script `deploy.sh` automatiza todo o processo de deploy.

### Configurar política de bucket

Aplique esta política para permitir acesso público:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::feature-flag-web/*"
        }
    ]
}
```

### URL de acesso

Após o deploy, o site estará disponível em:
```
http://feature-flag-web.s3-website-<região>.amazonaws.com
```

## Estrutura de Arquivos

```
web/
├── index.html      # Página principal
├── sso.js          # Lógica de autenticação SSO
├── README.md       # Este arquivo
└── deploy.sh       # Script de deploy
```

## localStorage

O site armazena os seguintes dados no localStorage:

- `featureFlag_userData`: Dados do usuário e tokens
- `featureFlag_lastLogin`: Data do último login

### Limpar dados

Para limpar os dados armazenados:

```javascript
localStorage.removeItem('featureFlag_userData');
localStorage.removeItem('featureFlag_lastLogin');
```

Ou use o botão "Sair" na interface.

## Troubleshooting

### Login não funciona

1. Verifique se o Client ID está correto
2. Verifique se os Redirect URIs estão configurados no Azure AD
3. Verifique o console do navegador para erros
4. Verifique se a biblioteca MSAL está carregada

### Token expirado

O token expira após 1 hora. O site tentará renovar automaticamente. Se falhar, faça logout e login novamente.

### CORS errors

Se estiver testando localmente com `file://`, use um servidor HTTP local (veja seção "Executar Localmente").

### Azure AD errors

Consulte a documentação oficial: https://docs.microsoft.com/azure/active-directory/develop/

## Segurança

- ⚠️ Nunca exponha o Client Secret (não necessário para SPA)
- ✅ Use HTTPS em produção
- ✅ Configure CORS adequadamente
- ✅ Tokens são armazenados no localStorage (considere usar sessionStorage para maior segurança)
- ✅ Implemente Content Security Policy (CSP)

## Próximos Passos

1. Configurar Azure AD
2. Testar autenticação
3. Fazer deploy no S3
4. Configurar domínio personalizado (opcional)
5. Implementar integração com a API Lambda
