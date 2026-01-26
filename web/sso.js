// sso.js
function login() {
    // Simula chamada OIDC e armazena credenciais fake
    const credentials = {
        access_token: 'fake-access-token',
        id_token: 'fake-id-token',
        expires_in: 3600
    };
    localStorage.setItem('sso_credentials', JSON.stringify(credentials));
    document.getElementById('result').innerText = 'Login realizado! Token salvo.';
}
