.PHONY: help install install-dev test test-verbose coverage clean deploy package lint format

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make test          - Run tests"
	@echo "  make test-verbose  - Run tests with verbose output"
	@echo "  make coverage      - Run tests with coverage report"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make package       - Create deployment package"
	@echo "  make deploy        - Deploy to AWS Lambda"
	@echo "  make lint          - Run linting (requires flake8)"
	@echo "  make format        - Format code (requires black)"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest

test-verbose:
	pytest -v

coverage:
	pytest --cov=src --cov=lambda_function --cov-report=term-missing --cov-report=html

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf src/*/__pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -f function.zip

package: clean
	mkdir -p build
	cp -r src build/
	cp lambda_function.py build/
	pip install -r requirements.txt -t build/
	cd build && zip -r ../function.zip . -q
	@echo "Package created: function.zip"

deploy: package
	@if [ -z "$(LAMBDA_ROLE_ARN)" ]; then \
		echo "Error: LAMBDA_ROLE_ARN environment variable is required"; \
		exit 1; \
	fi
	@bash deploy.sh

lint:
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 src tests lambda_function.py; \
	else \
		echo "flake8 not installed. Run: pip install flake8"; \
	fi

format:
	@if command -v black >/dev/null 2>&1; then \
		black src tests lambda_function.py; \
	else \
		echo "black not installed. Run: pip install black"; \
	fi
