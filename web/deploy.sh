#!/bin/bash
set -e
cd "$(dirname "$0")"
# Exemplo: aws s3 sync . s3://<bucket-name>/ --exclude "*.sh" --delete
# Configure o bucket e credenciais AWS antes de rodar
