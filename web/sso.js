// Configuração do Azure AD / Microsoft Identity Platform
const msalConfig = {
    auth: {
        clientId: "YOUR_CLIENT_ID", // Substitua pelo seu Client ID do Azure AD
        authority: "https://login.microsoftonline.com/common", // ou o Tenant ID específico
        redirectUri: window.location.origin // URL de redirecionamento
    },
    cache: {
        cacheLocation: "localStorage",
        storeAuthStateInCookie: false
    }
};

// Escopos solicitados
const loginRequest = {
    scopes: ["User.Read", "openid", "profile", "email"]
};

// Instância do MSAL (Microsoft Authentication Library)
let msalInstance;

// Elementos DOM
const loginSection = document.getElementById('loginSection');
const userInfo = document.getElementById('userInfo');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const btnLogin = document.getElementById('btnLogin');
const btnLogout = document.getElementById('btnLogout');
const btnCopyToken = document.getElementById('btnCopyToken');

// Inicializar MSAL
function initializeMsal() {
    try {
        // Verificar se MSAL está disponível
        if (typeof msal === 'undefined') {
            showError('MSAL library não carregada. Certifique-se de incluir o script MSAL no HTML.');
            showMockLogin();
            return;
        }

        msalInstance = new msal.PublicClientApplication(msalConfig);

        // Verificar se há uma sessão ativa
        handleRedirect();
    } catch (error) {
        console.error('Erro ao inicializar MSAL:', error);
        showError('Erro ao inicializar autenticação. Modo de demonstração ativado.');
        showMockLogin();
    }
}

// Lidar com redirecionamento após login
async function handleRedirect() {
    try {
        const response = await msalInstance.handleRedirectPromise();

        if (response) {
            // Login bem-sucedido via redirecionamento
            handleLoginSuccess(response);
        } else {
            // Verificar se já existe uma conta logada
            const accounts = msalInstance.getAllAccounts();
            if (accounts.length > 0) {
                // Usuário já está logado
                await acquireTokenSilent(accounts[0]);
            } else {
                // Verificar localStorage para dados mock
                checkLocalStorage();
            }
        }
    } catch (error) {
        console.error('Erro no redirecionamento:', error);
        showError(error.message);
        checkLocalStorage();
    }
}

// Fazer login
async function login() {
    try {
        showLoading(true);
        hideError();

        if (msalInstance) {
            // Login real com Microsoft
            await msalInstance.loginRedirect(loginRequest);
        } else {
            // Modo mock para demonstração
            mockLogin();
        }
    } catch (error) {
        console.error('Erro ao fazer login:', error);
        showError(error.message);
        showLoading(false);
    }
}

// Obter token silenciosamente
async function acquireTokenSilent(account) {
    try {
        showLoading(true);

        const response = await msalInstance.acquireTokenSilent({
            ...loginRequest,
            account: account
        });

        handleLoginSuccess(response);
    } catch (error) {
        console.error('Erro ao obter token:', error);

        // Se falhar, tentar login interativo
        if (error instanceof msal.InteractionRequiredAuthError) {
            await msalInstance.acquireTokenRedirect(loginRequest);
        } else {
            showError(error.message);
            showLoading(false);
        }
    }
}

// Lidar com sucesso do login
function handleLoginSuccess(response) {
    const account = response.account;
    const token = response.accessToken;

    // Dados do usuário
    const userData = {
        id: account.localAccountId,
        name: account.name,
        username: account.username,
        email: account.username,
        tenantId: account.tenantId,
        accessToken: token,
        idToken: response.idToken,
        expiresOn: response.expiresOn
    };

    // Salvar no localStorage
    saveToLocalStorage(userData);

    // Exibir dados do usuário
    displayUserInfo(userData);

    showLoading(false);
}

// Mock login para demonstração
function mockLogin() {
    setTimeout(() => {
        const mockData = {
            id: 'mock-user-' + Date.now(),
            name: 'Usuário Demonstração',
            username: 'usuario.demo@example.com',
            email: 'usuario.demo@example.com',
            tenantId: 'mock-tenant-id',
            accessToken: generateMockToken(),
            idToken: 'mock-id-token',
            expiresOn: new Date(Date.now() + 3600000).toISOString()
        };

        saveToLocalStorage(mockData);
        displayUserInfo(mockData);
        showLoading(false);
    }, 1500);
}

// Gerar token mock
function generateMockToken() {
    const header = btoa(JSON.stringify({ alg: 'RS256', typ: 'JWT' }));
    const payload = btoa(JSON.stringify({
        sub: 'mock-user-id',
        name: 'Usuário Demonstração',
        email: 'usuario.demo@example.com',
        iat: Math.floor(Date.now() / 1000),
        exp: Math.floor(Date.now() / 1000) + 3600
    }));
    const signature = btoa('mock-signature');

    return `${header}.${payload}.${signature}`;
}

// Exibir informações do usuário
function displayUserInfo(userData) {
    // Atualizar elementos
    document.getElementById('userName').textContent = userData.name;
    document.getElementById('userEmail').textContent = userData.email;
    document.getElementById('userId').textContent = userData.id;
    document.getElementById('userUsername').textContent = userData.username;
    document.getElementById('userTenant').textContent = userData.tenantId;
    document.getElementById('accessToken').textContent = userData.accessToken;

    // Avatar com iniciais
    const initials = userData.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
    document.getElementById('userAvatar').textContent = initials;

    // Mostrar seção de usuário
    loginSection.style.display = 'none';
    userInfo.classList.add('active');
}

// Salvar no localStorage
function saveToLocalStorage(userData) {
    try {
        localStorage.setItem('featureFlag_userData', JSON.stringify(userData));
        localStorage.setItem('featureFlag_lastLogin', new Date().toISOString());
    } catch (error) {
        console.error('Erro ao salvar no localStorage:', error);
    }
}

// Verificar localStorage
function checkLocalStorage() {
    try {
        const savedData = localStorage.getItem('featureFlag_userData');

        if (savedData) {
            const userData = JSON.parse(savedData);

            // Verificar se o token não expirou
            if (userData.expiresOn && new Date(userData.expiresOn) > new Date()) {
                displayUserInfo(userData);
            } else {
                // Token expirado, fazer logout
                logout();
            }
        }
    } catch (error) {
        console.error('Erro ao verificar localStorage:', error);
    }
}

// Fazer logout
function logout() {
    try {
        // Limpar localStorage
        localStorage.removeItem('featureFlag_userData');
        localStorage.removeItem('featureFlag_lastLogin');

        // Logout do MSAL se disponível
        if (msalInstance) {
            const accounts = msalInstance.getAllAccounts();
            if (accounts.length > 0) {
                msalInstance.logoutRedirect({
                    account: accounts[0]
                });
                return;
            }
        }

        // Recarregar página
        window.location.reload();
    } catch (error) {
        console.error('Erro ao fazer logout:', error);
        window.location.reload();
    }
}

// Copiar token
function copyToken() {
    const tokenText = document.getElementById('accessToken').textContent;

    navigator.clipboard.writeText(tokenText).then(() => {
        const btn = document.getElementById('btnCopyToken');
        const originalText = btn.textContent;
        btn.textContent = '✅ Copiado!';

        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    }).catch(error => {
        console.error('Erro ao copiar:', error);
        showError('Erro ao copiar token');
    });
}

// Mostrar/ocultar loading
function showLoading(show) {
    if (show) {
        loading.classList.add('active');
        loginSection.style.display = 'none';
        userInfo.classList.remove('active');
    } else {
        loading.classList.remove('active');
    }
}

// Mostrar erro
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.add('active');
}

// Ocultar erro
function hideError() {
    errorMessage.classList.remove('active');
}

// Mostrar login mock
function showMockLogin() {
    console.warn('Modo demonstração ativado. Para usar SSO real, configure o Azure AD e inclua a biblioteca MSAL.');
    // O botão de login já está visível, apenas funcionará em modo mock
}

// Event Listeners
btnLogin.addEventListener('click', login);
btnLogout.addEventListener('click', logout);
btnCopyToken.addEventListener('click', copyToken);

// Inicializar ao carregar a página
window.addEventListener('DOMContentLoaded', () => {
    // Para usar SSO real, descomente a linha abaixo e inclua a biblioteca MSAL no HTML
    // initializeMsal();

    // Modo demonstração (remova esta linha quando configurar SSO real)
    checkLocalStorage();
});
