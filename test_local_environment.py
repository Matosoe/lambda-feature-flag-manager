"""
Script de teste para validar o ambiente local do Feature Flag Manager
Execute após subir o ambiente com 'make up'
"""
import requests
import json
import sys
import subprocess

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def get_function_url():
    """Obtém a URL da função Lambda do LocalStack"""
    try:
        result = subprocess.run(
            ["aws", "--endpoint-url=http://localhost:4566", "lambda", 
             "get-function-url-config", "--function-name", "feature-flag-manager"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('FunctionUrl')
    except Exception as e:
        print(f"{RED}Erro ao obter URL da função: {e}{RESET}")
    return None

def print_test(name):
    print(f"\n{BLUE}🧪 Teste: {name}{RESET}")

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠ {message}{RESET}")

def test_list_parameters(base_url):
    """Testa listagem de parâmetros"""
    print_test("Listar todos os parâmetros")
    
    response = requests.get(
        f"{base_url}/parameters",
        headers={"X-User-Id": "dev@local.dev"}
    )
    
    if response.status_code == 200:
        data = response.json()
        params = data.get('parameters', [])
        print_success(f"Listagem bem-sucedida: {len(params)} parâmetros encontrados")
        for param in params[:3]:  # Mostra os 3 primeiros
            print(f"  - {param.get('id')}: {param.get('value')} ({param.get('type')})")
        return True
    else:
        print_error(f"Falha: {response.status_code} - {response.text}")
        return False

def test_get_parameter(base_url):
    """Testa obter parâmetro específico"""
    print_test("Obter parâmetro específico (DARK_MODE)")
    
    response = requests.get(
        f"{base_url}/parameters/DARK_MODE",
        headers={"X-User-Id": "dev@local.dev"}
    )
    
    if response.status_code == 200:
        data = response.json()
        print_success("Parâmetro obtido com sucesso")
        print(f"  ID: {data.get('id')}")
        print(f"  Value: {data.get('value')}")
        print(f"  Type: {data.get('type')}")
        return True
    else:
        print_error(f"Falha: {response.status_code} - {response.text}")
        return False

def test_create_parameter(base_url):
    """Testa criação de parâmetro"""
    print_test("Criar novo parâmetro")
    
    payload = {
        "id": "TEST_FEATURE",
        "value": "true",
        "type": "BOOLEAN",
        "description": "Feature de teste criada pelo script",
        "lastModifiedBy": "dev@local.dev",
        "prefix": "test"
    }
    
    response = requests.post(
        f"{base_url}/parameters",
        headers={
            "X-User-Id": "dev@local.dev",
            "Content-Type": "application/json"
        },
        json=payload
    )
    
    if response.status_code in [200, 201]:
        data = response.json()
        print_success(f"Parâmetro criado: {data.get('id')}")
        return True
    else:
        print_error(f"Falha: {response.status_code} - {response.text}")
        return False

def test_update_parameter(base_url):
    """Testa atualização de parâmetro"""
    print_test("Atualizar parâmetro")
    
    payload = {
        "value": "false",
        "description": "Feature de teste atualizada",
        "lastModifiedBy": "dev@local.dev",
        "prefix": "test"
    }
    
    response = requests.put(
        f"{base_url}/parameters/TEST_FEATURE",
        headers={
            "X-User-Id": "dev@local.dev",
            "Content-Type": "application/json"
        },
        json=payload
    )
    
    if response.status_code == 200:
        print_success("Parâmetro atualizado com sucesso")
        return True
    else:
        print_error(f"Falha: {response.status_code} - {response.text}")
        return False

def test_delete_parameter(base_url):
    """Testa deleção de parâmetro"""
    print_test("Deletar parâmetro")
    
    response = requests.delete(
        f"{base_url}/parameters/TEST_FEATURE",
        headers={"X-User-Id": "dev@local.dev"}
    )
    
    if response.status_code == 200:
        print_success("Parâmetro deletado com sucesso")
        return True
    else:
        print_error(f"Falha: {response.status_code} - {response.text}")
        return False

def test_list_users(base_url):
    """Testa listagem de usuários"""
    print_test("Listar usuários (apenas admin)")
    
    response = requests.get(
        f"{base_url}/users",
        headers={"X-User-Id": "admin@local.dev"}
    )
    
    if response.status_code == 200:
        data = response.json()
        users = data.get('usuarios', [])
        print_success(f"Listagem bem-sucedida: {len(users)} usuários encontrados")
        for user in users:
            print(f"  - {user.get('id')}: {user.get('nome')}")
        return True
    else:
        print_error(f"Falha: {response.status_code} - {response.text}")
        return False

def test_permissions(base_url):
    """Testa sistema de permissões"""
    print_test("Validar permissões (analista tentando criar parâmetro)")
    
    payload = {
        "id": "UNAUTHORIZED_TEST",
        "value": "true",
        "type": "BOOLEAN",
        "description": "Este parâmetro não deveria ser criado",
        "lastModifiedBy": "analista@local.dev"
    }
    
    response = requests.post(
        f"{base_url}/parameters",
        headers={
            "X-User-Id": "analista@local.dev",
            "Content-Type": "application/json"
        },
        json=payload
    )
    
    # Deve falhar com 403
    if response.status_code == 403:
        print_success("Permissões funcionando corretamente (acesso negado)")
        return True
    else:
        print_warning(f"Esperado 403, recebido {response.status_code}")
        return False

def main():
    print(f"{BLUE}{'='*60}")
    print("Feature Flag Manager - Testes de Validação do Ambiente Local")
    print(f"{'='*60}{RESET}\n")
    
    # Obter URL da função
    print("🔍 Procurando URL da função Lambda...")
    base_url = get_function_url()
    
    if not base_url:
        print_error("Não foi possível obter a URL da função Lambda")
        print_warning("Certifique-se de que o ambiente está rodando: make up")
        sys.exit(1)
    
    print_success(f"URL encontrada: {base_url}\n")
    
    # Executar testes
    results = []
    
    results.append(("Listar parâmetros", test_list_parameters(base_url)))
    results.append(("Obter parâmetro", test_get_parameter(base_url)))
    results.append(("Criar parâmetro", test_create_parameter(base_url)))
    results.append(("Atualizar parâmetro", test_update_parameter(base_url)))
    results.append(("Deletar parâmetro", test_delete_parameter(base_url)))
    results.append(("Listar usuários", test_list_users(base_url)))
    results.append(("Testar permissões", test_permissions(base_url)))
    
    # Resumo
    print(f"\n{BLUE}{'='*60}")
    print("Resumo dos Testes")
    print(f"{'='*60}{RESET}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}✓ PASSOU{RESET}" if result else f"{RED}✗ FALHOU{RESET}"
        print(f"  {test_name}: {status}")
    
    print(f"\n{BLUE}Total: {passed}/{total} testes passaram{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}🎉 Todos os testes passaram! Ambiente funcionando perfeitamente!{RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{YELLOW}⚠️  Alguns testes falharam. Verifique os logs acima.{RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
