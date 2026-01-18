#!/usr/bin/env python3
"""
Proxy HTTP para Swagger UI
Converte requisições HTTP do browser em invocações da Lambda no LocalStack
"""

import json
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class LambdaProxyHandler(BaseHTTPRequestHandler):
    """Handler que converte requisições HTTP em invocações Lambda"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        # Criar payload Lambda
        lambda_payload = {
            "httpMethod": "GET",
            "path": path,
            "headers": dict(self.headers),
            "queryStringParameters": {k: v[0] for k, v in query_params.items()} if query_params else {}
        }
        
        try:
            # Invocar Lambda via docker exec
            cmd = [
                "docker", "exec", "feature-flag-localstack",
                "sh", "-c",
                f"awslocal lambda invoke "
                f"--function-name feature-flag-manager "
                f"--payload '{json.dumps(lambda_payload)}' "
                f"/tmp/proxy_response.json > /dev/null 2>&1 && cat /tmp/proxy_response.json"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                self.send_error(500, f"Lambda invocation failed: {result.stderr}")
                return
            
            # Parse resposta da Lambda
            lambda_response = json.loads(result.stdout)
            
            # Enviar resposta HTTP
            status_code = lambda_response.get("statusCode", 200)
            headers = lambda_response.get("headers", {})
            body = lambda_response.get("body", "")
            
            self.send_response(status_code)
            for header_name, header_value in headers.items():
                self.send_header(header_name, header_value)
            self.end_headers()

            print(f"[PROXY] GET {path} -> {status_code}")
            
            # Escrever body
            if isinstance(body, str):
                self.wfile.write(body.encode('utf-8'))
            else:
                self.wfile.write(json.dumps(body).encode('utf-8'))
                
        except subprocess.TimeoutExpired:
            self.send_error(504, "Lambda invocation timeout")
            print(f"[PROXY] GET {path} -> 504 (timeout)")
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")
            print(f"[PROXY] GET {path} -> 500 ({str(e)})")
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""
        
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Criar payload Lambda
        lambda_payload = {
            "httpMethod": "POST",
            "path": path,
            "headers": dict(self.headers),
            "body": body
        }
        
        try:
            # Invocar Lambda
            cmd = [
                "docker", "exec", "feature-flag-localstack",
                "sh", "-c",
                f"awslocal lambda invoke "
                f"--function-name feature-flag-manager "
                f"--payload '{json.dumps(lambda_payload)}' "
                f"/tmp/proxy_response.json > /dev/null 2>&1 && cat /tmp/proxy_response.json"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                self.send_error(500, f"Lambda invocation failed: {result.stderr}")
                return
            
            # Parse resposta
            lambda_response = json.loads(result.stdout)
            
            # Enviar resposta HTTP
            status_code = lambda_response.get("statusCode", 200)
            headers = lambda_response.get("headers", {})
            body_response = lambda_response.get("body", "")
            
            self.send_response(status_code)
            for header_name, header_value in headers.items():
                self.send_header(header_name, header_value)
            self.end_headers()
            
            if isinstance(body_response, str):
                self.wfile.write(body_response.encode('utf-8'))
            else:
                self.wfile.write(json.dumps(body_response).encode('utf-8'))

            print(f"[PROXY] POST {path} -> {status_code}")
                
        except subprocess.TimeoutExpired:
            self.send_error(504, "Lambda invocation timeout")
            print(f"[PROXY] POST {path} -> 504 (timeout)")
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")
            print(f"[PROXY] POST {path} -> 500 ({str(e)})")
    
    def do_PUT(self):
        """Handle PUT requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""

        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # Criar payload Lambda
        lambda_payload = {
            "httpMethod": "PUT",
            "path": path,
            "headers": dict(self.headers),
            "body": body
        }

        try:
            # Invocar Lambda
            cmd = [
                "docker", "exec", "feature-flag-localstack",
                "sh", "-c",
                f"awslocal lambda invoke "
                f"--function-name feature-flag-manager "
                f"--payload '{json.dumps(lambda_payload)}' "
                f"/tmp/proxy_response.json > /dev/null 2>&1 && cat /tmp/proxy_response.json"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

            if result.returncode != 0:
                self.send_error(500, f"Lambda invocation failed: {result.stderr}")
                return

            # Parse resposta
            lambda_response = json.loads(result.stdout)

            # Enviar resposta HTTP
            status_code = lambda_response.get("statusCode", 200)
            headers = lambda_response.get("headers", {})
            body_response = lambda_response.get("body", "")

            self.send_response(status_code)
            for header_name, header_value in headers.items():
                self.send_header(header_name, header_value)
            self.end_headers()

            if isinstance(body_response, str):
                self.wfile.write(body_response.encode('utf-8'))
            else:
                self.wfile.write(json.dumps(body_response).encode('utf-8'))

            print(f"[PROXY] PUT {path} -> {status_code}")

        except subprocess.TimeoutExpired:
            self.send_error(504, "Lambda invocation timeout")
            print(f"[PROXY] PUT {path} -> 504 (timeout)")
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")
            print(f"[PROXY] PUT {path} -> 500 ({str(e)})")
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        lambda_payload = {
            "httpMethod": "DELETE",
            "path": path,
            "headers": dict(self.headers)
        }
        
        try:
            cmd = [
                "docker", "exec", "feature-flag-localstack",
                "sh", "-c",
                f"awslocal lambda invoke "
                f"--function-name feature-flag-manager "
                f"--payload '{json.dumps(lambda_payload)}' "
                f"/tmp/proxy_response.json > /dev/null 2>&1 && cat /tmp/proxy_response.json"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                self.send_error(500, f"Lambda invocation failed")
                return
            
            lambda_response = json.loads(result.stdout)
            
            status_code = lambda_response.get("statusCode", 200)
            headers = lambda_response.get("headers", {})
            body = lambda_response.get("body", "")
            
            self.send_response(status_code)
            for header_name, header_value in headers.items():
                self.send_header(header_name, header_value)
            self.end_headers()
            
            if isinstance(body, str):
                self.wfile.write(body.encode('utf-8'))
            else:
                self.wfile.write(json.dumps(body).encode('utf-8'))

            print(f"[PROXY] DELETE {path} -> {status_code}")
                
        except subprocess.TimeoutExpired:
            self.send_error(504, "Lambda invocation timeout")
            print(f"[PROXY] DELETE {path} -> 504 (timeout)")
        except Exception as e:
            self.send_error(500, f"Error: {str(e)}")
            print(f"[PROXY] DELETE {path} -> 500 ({str(e)})")
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.log_date_time_string()}] {format % args}")


def main():
    port = 8080
    server_address = ('', port)
    httpd = HTTPServer(server_address, LambdaProxyHandler)
    
    print("=" * 60)
    print("🚀 Feature Flag Manager - Swagger UI Proxy")
    print("=" * 60)
    print(f"\n✅ Servidor rodando em http://localhost:{port}")
    print(f"\n📖 Acesse o Swagger UI:")
    print(f"   👉 http://localhost:{port}/")
    print(f"\n🔍 Endpoints disponíveis:")
    print(f"   • http://localhost:{port}/        - Swagger UI (interface web)")
    print(f"   • http://localhost:{port}/docs    - OpenAPI Specification (JSON)")
    print(f"   • http://localhost:{port}/health  - Health Check")
    print(f"\n📝 API Endpoints:")
    print(f"   • GET/POST http://localhost:{port}/parameters")
    print(f"   • GET/PUT/DELETE http://localhost:{port}/parameters/{{id}}")
    print(f"   • GET/POST http://localhost:{port}/users")
    print(f"   • GET/PUT/DELETE http://localhost:{port}/users/{{id}}")
    print(f"\n🔑 Não esqueça de adicionar o header:")
    print(f"   X-User-Id: dev@local.dev")
    print(f"\n💡 O Swagger UI já adiciona esse header automaticamente!")
    print(f"\n⏹️  Pressione Ctrl+C para parar o servidor")
    print("=" * 60)
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor parado.")
        sys.exit(0)


if __name__ == "__main__":
    main()
