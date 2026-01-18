#!/bin/bash

# Teste completo da API (parameters e users) com cenários OK e não OK.

set -u

BASE_URL=${BASE_URL:-http://localhost:8080}

if ! command -v curl &> /dev/null; then
    echo "[FATAL] curl não encontrado. Instale o curl para executar os testes."
    exit 1
fi

RUN_ID=$(date +%s)
TEST_PARAM_ID="TEST_PARAM_OK_$RUN_ID"
TEST_USER_ID="test.user+$RUN_ID@local.dev"

UNAME_OUT=$(uname -s 2>/dev/null || true)
IS_WINDOWS=0
case "$UNAME_OUT" in
    MINGW*|MSYS*|CYGWIN*) IS_WINDOWS=1 ;;
esac

url_encode() {
    if [ "$IS_WINDOWS" -eq 1 ] && command -v powershell &> /dev/null; then
        powershell -NoProfile -Command "[uri]::EscapeDataString(\"$1\")"
        return 0
    fi
    if command -v python3 &> /dev/null; then
        python3 -V >/dev/null 2>&1 && python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$1" && return 0
    fi
    if command -v python &> /dev/null; then
        python -V >/dev/null 2>&1 && python -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$1" && return 0
    fi
    if command -v py &> /dev/null; then
        py -3 -V >/dev/null 2>&1 && py -3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$1" && return 0
    fi
    if command -v powershell &> /dev/null; then
        powershell -NoProfile -Command "[uri]::EscapeDataString(\"$1\")"
        return 0
    fi
    echo "[FATAL] Nenhum utilitário disponível para URL-encode (python/py/powershell)."
    exit 1
}

failures=0

request() {
    local method=$1
    local url=$2
    local data=${3:-}
    shift 3 || true

    local resp_file
    resp_file=$(mktemp)
    local err_file
    err_file=$(mktemp)

    local curl_args=( -s -o "$resp_file" -w "%{http_code}" -X "$method" "$url" )
    while [ $# -gt 0 ]; do
        curl_args+=( -H "$1" )
        shift
    done

    if [ -n "$data" ]; then
        curl_args+=( -d "$data" )
    fi

    local attempts=0
    local status
    local curl_exit
    local body
    local err

    while [ $attempts -lt 3 ]; do
        status=$(curl "${curl_args[@]}" 2>"$err_file")
        curl_exit=$?
        body=$(cat "$resp_file")
        err=$(cat "$err_file")

        if [ $curl_exit -eq 0 ] && [ "$status" != "000" ]; then
            rm -f "$resp_file" "$err_file"
            echo "$status"$'\n'"$body"
            return
        fi

        attempts=$((attempts+1))
        sleep 0.5
    done

    rm -f "$resp_file" "$err_file"
    echo "000"$'\n'"curl_error (exit=$curl_exit): $err"
}

assert_status() {
    local test_name=$1
    local expected=$2
    local status=$3
    local body=$4

    if [ "$status" != "$expected" ]; then
        echo "[FAIL] $test_name"
        echo "       expected: $expected"
        echo "       got:      $status"
        echo "       body:     $body"
        failures=$((failures+1))
    else
        echo "[OK]   $test_name"
    fi
}

# =====================
# Parameters
# =====================

# 1) List OK
resp=$(request GET "$BASE_URL/parameters" "" "X-User-Id: dev@local.dev")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "parameters:list_ok" "200" "$status" "$body"

# 2) List not OK (missing header)
resp=$(request GET "$BASE_URL/parameters")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "parameters:list_no_header" "403" "$status" "$body"

# 3) Get OK
resp=$(request GET "$BASE_URL/parameters/ui%2FDARK_MODE" "" "X-User-Id: dev@local.dev")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "parameters:get_ok" "200" "$status" "$body"

# 4) Get not OK
resp=$(request GET "$BASE_URL/parameters/NOT_FOUND_PARAM" "" "X-User-Id: dev@local.dev")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "parameters:get_not_found" "404" "$status" "$body"

# 5) Create OK
create_payload='{"id":"'$TEST_PARAM_ID'","value":"true","type":"BOOLEAN","description":"Teste OK","lastModifiedBy":"dev@local.dev","prefix":"test"}'
resp=$(request POST "$BASE_URL/parameters" "$create_payload" "X-User-Id: dev@local.dev" "Content-Type: application/json")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
if [ "$status" != "201" ] && [ "$status" != "200" ]; then
    assert_status "parameters:create_ok" "201/200" "$status" "$body"
else
    echo "[OK]   parameters:create_ok"
fi

# 6) Create not OK (sem permissão)
create_payload_unauth='{"id":"UNAUTHORIZED_PARAM","value":"true","type":"BOOLEAN","description":"Teste sem permissao","lastModifiedBy":"analista@local.dev"}'
resp=$(request POST "$BASE_URL/parameters" "$create_payload_unauth" "X-User-Id: analista@local.dev" "Content-Type: application/json" "accept: */*")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "parameters:create_forbidden" "403" "$status" "$body"

# 7) Update OK
update_payload='{"value":"false","description":"Atualizado"}'
resp=$(request PUT "$BASE_URL/parameters/test%2F$TEST_PARAM_ID" "$update_payload" "X-User-Id: dev@local.dev" "Content-Type: application/json")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "parameters:update_ok" "200" "$status" "$body"

# 8) Update not OK (JSON inválido)
update_payload_invalid='{"value":"false",}'
resp=$(request PUT "$BASE_URL/parameters/test%2F$TEST_PARAM_ID" "$update_payload_invalid" "X-User-Id: dev@local.dev" "Content-Type: application/json")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "parameters:update_invalid_json" "400" "$status" "$body"

# 9) Delete not OK (sem permissão) - parâmetro existente
arn_forbidden="arn:aws:ssm:us-east-1:000000000000:parameter/feature-flags/flags/contingencia/CONTINGENCIA_TOTAL"
encoded_arn_forbidden=$(url_encode "$arn_forbidden")
resp=$(request DELETE "$BASE_URL/parameters/arn/$encoded_arn_forbidden" "" "X-User-Id: dev@local.dev")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "parameters:delete_forbidden" "403" "$status" "$body"

# 10) Delete OK
arn_ok="arn:aws:ssm:us-east-1:000000000000:parameter/feature-flags/flags/test/$TEST_PARAM_ID"
encoded_arn_ok=$(url_encode "$arn_ok")
resp=$(request DELETE "$BASE_URL/parameters/arn/$encoded_arn_ok" "" "X-User-Id: admin@local.dev")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "parameters:delete_ok" "200" "$status" "$body"

# =====================
# Users
# =====================

# 11) List OK
resp=$(request GET "$BASE_URL/users" "" "X-User-Id: admin@local.dev")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "users:list_ok" "200" "$status" "$body"

# 12) List not OK (missing header)
resp=$(request GET "$BASE_URL/users")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "users:list_no_header" "403" "$status" "$body"

# 13) Create OK
user_payload='{"id":"'$TEST_USER_ID'","nome":"Usuario Teste","permissoes":{"leitura":true,"escrita":true,"admin":false},"ativo":true}'
resp=$(request POST "$BASE_URL/users" "$user_payload" "X-User-Id: admin@local.dev" "Content-Type: application/json")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "users:create_ok" "201" "$status" "$body"

# 14) Create not OK (JSON inválido)
user_payload_invalid='{"id":"x",}'
resp=$(request POST "$BASE_URL/users" "$user_payload_invalid" "X-User-Id: admin@local.dev" "Content-Type: application/json")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "users:create_invalid_json" "400" "$status" "$body"

# 14.1) Create not OK (missing body)
resp=$(request POST "$BASE_URL/users" "" "X-User-Id: admin@local.dev" "Content-Type: application/json")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "users:create_missing_body" "400" "$status" "$body"

# 15) Get OK
encoded_user_id=$(url_encode "$TEST_USER_ID")
resp=$(request GET "$BASE_URL/users/$encoded_user_id" "" "X-User-Id: admin@local.dev")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "users:get_ok" "200" "$status" "$body"

# 16) Update OK
user_update_payload='{"nome":"Usuario Teste Atualizado","ativo":true}'
resp=$(request PUT "$BASE_URL/users/$encoded_user_id" "$user_update_payload" "X-User-Id: admin@local.dev" "Content-Type: application/json")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "users:update_ok" "200" "$status" "$body"

# 17) Update not OK (sem permissão)
resp=$(request PUT "$BASE_URL/users/$encoded_user_id" "$user_update_payload" "X-User-Id: dev@local.dev" "Content-Type: application/json")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "users:update_forbidden" "403" "$status" "$body"

# 18) Delete not OK (sem permissão)
resp=$(request DELETE "$BASE_URL/users/$encoded_user_id" "" "X-User-Id: dev@local.dev")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "users:delete_forbidden" "403" "$status" "$body"

# 19) Delete OK
resp=$(request DELETE "$BASE_URL/users/$encoded_user_id" "" "X-User-Id: admin@local.dev")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "users:delete_ok" "200" "$status" "$body"

# 20) Get not OK (após delete)
resp=$(request GET "$BASE_URL/users/$encoded_user_id" "" "X-User-Id: admin@local.dev")
status=$(echo "$resp" | head -n1)
body=$(echo "$resp" | tail -n +2)
assert_status "users:get_not_found" "404" "$status" "$body"

# =====================
# Resumo
# =====================

if [ $failures -eq 0 ]; then
    echo ""
    echo "✅ Todos os testes passaram."
    exit 0
else
    echo ""
    echo "❌ Falhas encontradas: $failures"
    exit 1
fi
