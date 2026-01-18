.PHONY: help build up down restart logs logs-lambda clean test-api test-python install-dev validate

help: ## Mostra esta mensagem de ajuda
	@echo "Feature Flag Manager - Comandos disponíveis:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

validate: ## Valida se o ambiente está configurado corretamente
	@chmod +x validate_environment.sh
	@./validate_environment.sh

build: ## Builda as imagens Docker
	@echo "🔨 Buildando imagens..."
	docker-compose build
	@echo "✓ Build concluído"

up: ## Sobe o ambiente LocalStack + Lambda
	@echo "🚀 Subindo ambiente..."
	@chmod +x init-localstack.sh
	docker-compose up -d
	@echo ""
	@echo "⏳ Aguardando LocalStack inicializar (30s)..."
	@sleep 30
	@echo ""
	@echo "✓ Ambiente pronto!"
	@echo ""
	@$(MAKE) info

down: ## Para e remove os containers
	@echo "🛑 Parando ambiente..."
	docker-compose down
	@echo "✓ Ambiente parado"

restart: ## Reinicia o ambiente
	@$(MAKE) down
	@$(MAKE) up

logs: ## Mostra logs do LocalStack
	docker-compose logs -f localstack

logs-lambda: ## Mostra logs da Lambda no LocalStack
	aws --endpoint-url=http://localhost:4566 logs tail /aws/lambda/feature-flag-manager --follow

clean: ## Remove containers, volumes e dados
	@echo "🧹 Limpando ambiente..."
	docker-compose down -v
	rm -rf localstack-data
	@echo "✓ Limpeza concluída"

info: ## Mostra informações do ambiente
	@echo "==================================="
	@echo "Feature Flag Manager - Ambiente Local"
	@echo "==================================="
	@echo ""
	@echo "📍 Endpoint LocalStack: http://localhost:4566"
	@echo ""
	@FUNCTION_URL=$$(aws --endpoint-url=http://localhost:4566 lambda get-function-url-config --function-name feature-flag-manager --query 'FunctionUrl' --output text 2>/dev/null); \
	if [ -n "$$FUNCTION_URL" ]; then \
		echo "📍 Lambda Function URL: $$FUNCTION_URL"; \
	else \
		echo "⚠️  Lambda Function URL ainda não disponível"; \
	fi
	@echo ""
	@echo "👥 Usuários disponíveis:"
	@echo "  - admin@local.dev (todas permissões)"
	@echo "  - dev@local.dev (leitura + escrita)"
	@echo "  - analista@local.dev (apenas leitura)"
	@echo ""
	@echo "📚 Comandos úteis:"
	@echo "  make test-api    - Testa a API (curl)"
	@echo "  make test-python - Testa a API (Python)"
	@echo "  make logs        - Ver logs do LocalStack"
	@echo "  make logs-lambda - Ver logs da Lambda"
	@echo ""
	@echo "==================================="

test-api: ## Testa a API localmente (usando curl)
	@echo "🧪 Testando API..."
	@echo ""
	@FUNCTION_URL=$$(aws --endpoint-url=http://localhost:4566 lambda get-function-url-config --function-name feature-flag-manager --query 'FunctionUrl' --output text 2>/dev/null); \
	if [ -z "$$FUNCTION_URL" ]; then \
		echo "❌ Lambda Function URL não disponível. Execute 'make up' primeiro."; \
		exit 1; \
	fi; \
	echo "1. Listando parâmetros..."; \
	curl -s -X GET "$$FUNCTION_URL/parameters" -H "X-User-Id: dev@local.dev" | python -m json.tool; \
	echo ""; echo ""; \
	echo "2. Obtendo parâmetro específico (DARK_MODE)..."; \
	curl -s -X GET "$$FUNCTION_URL/parameters/DARK_MODE" -H "X-User-Id: dev@local.dev" | python -m json.tool; \
	echo ""; echo ""; \
	echo "3. Listando usuários..."; \
	curl -s -X GET "$$FUNCTION_URL/users" -H "X-User-Id: admin@local.dev" | python -m json.tool; \
	echo ""; echo ""; \
	echo "✓ Testes concluídos"

test-python: install-dev ## Executa suite de testes Python completa
	@echo "🐍 Executando testes Python..."
	@python test_local_environment.py

install-dev: ## Instala dependências de desenvolvimento
	@echo "📦 Instalando dependências de desenvolvimento..."
	@pip install -r requirements-dev.txt
	@echo "✓ Dependências instaladas"

install-aws-cli: ## Instala AWS CLI local (awslocal)
	@echo "📦 Instalando awslocal..."
	pip install awscli-local
	@echo "✓ awslocal instalado. Use 'awslocal' para interagir com LocalStack"
