"""
Swagger UI Handler
Serve a interface web do Swagger UI para documentação interativa da API
"""
import json
import os
from pathlib import Path


def get_openapi_spec() -> dict:
    """
    Retorna a especificação OpenAPI embutida no código
    """
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Feature Flag Manager API",
            "description": "API REST para gerenciamento de feature flags com suporte a usuários e permissões.\n\n## Autenticação\nTodas as requisições requerem o header `X-User-Id` com o email do usuário.\n\n## Permissões\n- **leitura**: Visualizar parâmetros e usuários\n- **escrita**: Criar e atualizar parâmetros\n- **admin**: Acesso completo incluindo gerenciamento de usuários",
            "version": "2.0.0"
        },
        "servers": [
            {"url": "http://localhost:4566/2021-10-31/functions/feature-flag-manager/invocations", "description": "LocalStack (Desenvolvimento Local)"}
        ],
        "tags": [
            {"name": "Parameters", "description": "Operações com feature flags"},
            {"name": "Users", "description": "Gerenciamento de usuários e permissões"},
            {"name": "System", "description": "Endpoints do sistema"}
        ],
        "paths": {
            "/": {
                "get": {
                    "tags": ["System"],
                    "summary": "Documentação Swagger UI",
                    "responses": {"200": {"description": "Interface HTML do Swagger UI"}}
                }
            },
            "/docs": {
                "get": {
                    "tags": ["System"],
                    "summary": "Especificação OpenAPI (JSON)",
                    "responses": {"200": {"description": "Especificação OpenAPI"}}
                }
            },
            "/health": {
                "get": {
                    "tags": ["System"],
                    "summary": "Health Check",
                    "responses": {
                        "200": {
                            "description": "API está saudável",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string", "example": "healthy"},
                                            "timestamp": {"type": "string", "format": "date-time"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/parameters": {
                "get": {
                    "tags": ["Parameters"],
                    "summary": "Listar feature flags",
                    "description": "Lista todos os feature flags do Parameter Store",
                    "security": [{"UserAuth": []}],
                    "parameters": [{"$ref": "#/components/parameters/UserIdHeader"}],
                    "responses": {
                        "200": {"description": "Lista de parâmetros"},
                        "403": {"$ref": "#/components/responses/Forbidden"}
                    }
                },
                "post": {
                    "tags": ["Parameters"],
                    "summary": "Criar feature flag",
                    "description": "Cria um novo feature flag",
                    "security": [{"UserAuth": []}],
                    "parameters": [{"$ref": "#/components/parameters/UserIdHeader"}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/CreateParameterRequest"},
                                "examples": {
                                    "boolean": {
                                        "summary": "Feature flag booleana",
                                        "value": {
                                            "id": "DARK_MODE",
                                            "value": "true",
                                            "type": "BOOLEAN",
                                            "description": "Habilita modo escuro",
                                            "lastModifiedBy": "dev@local.dev",
                                            "prefix": "ui"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "Parâmetro criado"},
                        "400": {"$ref": "#/components/responses/BadRequest"},
                        "403": {"$ref": "#/components/responses/Forbidden"}
                    }
                }
            },
            "/parameters/{parameterId}": {
                "get": {
                    "tags": ["Parameters"],
                    "summary": "Obter feature flag específica",
                    "security": [{"UserAuth": []}],
                    "parameters": [
                        {"$ref": "#/components/parameters/UserIdHeader"},
                        {"name": "parameterId", "in": "path", "required": True, "schema": {"type": "string"}, "example": "DARK_MODE"}
                    ],
                    "responses": {"200": {"description": "Detalhes do parâmetro"}}
                },
                "put": {
                    "tags": ["Parameters"],
                    "summary": "Atualizar feature flag",
                    "security": [{"UserAuth": []}],
                    "parameters": [
                        {"$ref": "#/components/parameters/UserIdHeader"},
                        {"name": "parameterId", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {"200": {"description": "Parâmetro atualizado"}}
                },
                "delete": {
                    "tags": ["Parameters"],
                    "summary": "Deletar feature flag",
                    "security": [{"UserAuth": []}],
                    "parameters": [
                        {"$ref": "#/components/parameters/UserIdHeader"},
                        {"name": "parameterId", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {"200": {"description": "Parâmetro deletado"}}
                }
            },
            "/users": {
                "get": {
                    "tags": ["Users"],
                    "summary": "Listar usuários",
                    "security": [{"UserAuth": []}],
                    "parameters": [{"$ref": "#/components/parameters/UserIdHeader"}],
                    "responses": {"200": {"description": "Lista de usuários"}}
                },
                "post": {
                    "tags": ["Users"],
                    "summary": "Criar usuário",
                    "description": "Requer permissão admin",
                    "security": [{"UserAuth": []}],
                    "parameters": [{"$ref": "#/components/parameters/UserIdHeader"}],
                    "responses": {"201": {"description": "Usuário criado"}}
                }
            },
            "/users/{userId}": {
                "get": {
                    "tags": ["Users"],
                    "summary": "Obter usuário específico",
                    "security": [{"UserAuth": []}],
                    "parameters": [
                        {"$ref": "#/components/parameters/UserIdHeader"},
                        {"name": "userId", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {"200": {"description": "Detalhes do usuário"}}
                },
                "put": {
                    "tags": ["Users"],
                    "summary": "Atualizar usuário",
                    "security": [{"UserAuth": []}],
                    "parameters": [
                        {"$ref": "#/components/parameters/UserIdHeader"},
                        {"name": "userId", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {"200": {"description": "Usuário atualizado"}}
                },
                "delete": {
                    "tags": ["Users"],
                    "summary": "Deletar usuário",
                    "security": [{"UserAuth": []}],
                    "parameters": [
                        {"$ref": "#/components/parameters/UserIdHeader"},
                        {"name": "userId", "in": "path", "required": True, "schema": {"type": "string"}}
                    ],
                    "responses": {"200": {"description": "Usuário deletado"}}
                }
            }
        },
        "components": {
            "securitySchemes": {
                "UserAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-User-Id",
                    "description": "Email do usuário"
                }
            },
            "parameters": {
                "UserIdHeader": {
                    "name": "X-User-Id",
                    "in": "header",
                    "required": True,
                    "description": "Email do usuário",
                    "schema": {"type": "string", "format": "email"},
                    "example": "dev@local.dev"
                }
            },
            "schemas": {
                "CreateParameterRequest": {
                    "type": "object",
                    "required": ["id", "value", "type", "lastModifiedBy"],
                    "properties": {
                        "id": {"type": "string", "example": "MY_FEATURE"},
                        "value": {"type": "string", "example": "true"},
                        "type": {"type": "string", "enum": ["BOOLEAN", "STRING", "INTEGER", "DOUBLE", "DATE", "TIME", "DATETIME", "JSON"]},
                        "description": {"type": "string"},
                        "lastModifiedBy": {"type": "string", "format": "email"},
                        "prefix": {"type": "string"}
                    }
                }
            },
            "responses": {
                "BadRequest": {"description": "Requisição inválida"},
                "Forbidden": {"description": "Permissão negada"},
                "NotFound": {"description": "Recurso não encontrado"}
            }
        }
    }


def get_swagger_html(spec_url: str = "/docs") -> str:
    """
    Retorna o HTML do Swagger UI
    
    Args:
        spec_url: URL onde a especificação OpenAPI está disponível
    """
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feature Flag Manager API - Swagger UI</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.10.5/swagger-ui.css">
    <style>
        html {{ box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }}
        *, *:before, *:after {{ box-sizing: inherit; }}
        body {{ margin: 0; padding: 0; background: #fafafa; }}
        .swagger-ui .topbar {{ background-color: #2c3e50; }}
        .swagger-ui .topbar .download-url-wrapper {{ display: none; }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.10.5/swagger-ui-bundle.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.10.5/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            const ui = SwaggerUIBundle({{
                url: "{spec_url}",
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                defaultModelsExpandDepth: 1,
                defaultModelExpandDepth: 1,
                docExpansion: "list",
                filter: true,
                showRequestHeaders: true,
                tryItOutEnabled: true,
                requestInterceptor: (req) => {{
                    // Adicionar header padrão se não existir
                    if (!req.headers['X-User-Id']) {{
                        req.headers['X-User-Id'] = 'dev@local.dev';
                    }}
                    return req;
                }},
                onComplete: function() {{
                    console.log('Swagger UI carregado com sucesso!');
                    
                    // Adicionar informações na topbar
                    const topbar = document.querySelector('.topbar');
                    if (topbar) {{
                        const info = document.createElement('div');
                        info.style.cssText = 'color: white; padding: 10px 20px; font-size: 14px;';
                        info.innerHTML = `
                            <strong>🚀 Feature Flag Manager API</strong> - 
                            <span style="color: #7fba00;">LocalStack Development Environment</span>
                        `;
                        topbar.insertBefore(info, topbar.firstChild);
                    }}
                }}
            }});
            
            window.ui = ui;
        }};
    </script>
</body>
</html>'''


def handle_swagger_request(path: str) -> dict:
    """
    Processa requisições relacionadas ao Swagger
    
    Args:
        path: Caminho da requisição
        
    Returns:
        Resposta HTTP apropriada
    """
    # Rota raiz - Serve o Swagger UI
    if path == "/" or path == "":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html; charset=utf-8",
                "Cache-Control": "no-cache"
            },
            "body": get_swagger_html()
        }
    
    # Rota /docs - Especificação OpenAPI em JSON
    elif path == "/docs":
        spec = get_openapi_spec()
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(spec, ensure_ascii=False)
        }
    
    # Rota /health - Health check
    elif path == "/health":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "status": "healthy",
                "service": "feature-flag-manager",
                "swagger_ui": "available at /"
            })
        }
    
    return None
