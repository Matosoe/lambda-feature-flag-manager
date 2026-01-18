"""
Router for API endpoints
"""
import json
import logging
from typing import Dict, Any
from urllib.parse import unquote
from src.controllers.parameter_controller import ParameterController
from src.controllers.user_controller import UserController
from src.services.parameter_service import ParameterService
from src.services.user_service import UserService
from src.repositories.user_repository import UserRepository
from src.middlewares.authorization import AuthorizationMiddleware
from src.swagger_handler import handle_swagger_request
from src.exceptions import ValidationError

logger = logging.getLogger(__name__)


class Router:
    """
    Routes HTTP requests to appropriate controllers with authorization
    """
    
    def __init__(self, service: ParameterService):
        self.parameter_controller = ParameterController(service)
        
        # Initialize user-related components
        user_repository = UserRepository()
        user_service = UserService(user_repository)
        self.user_controller = UserController(user_service)
        self.auth_middleware = AuthorizationMiddleware(user_repository)
    
    def route(self, method: str, path: str, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route request to appropriate controller method with authorization
        
        Args:
            method: HTTP method
            path: Request path
            event: Complete API Gateway event
            
        Returns:
            API Gateway response
        """
        try:
            # Swagger UI routes (sem autenticação)
            if method == 'GET' and path in ['/', '', '/docs', '/health']:
                swagger_response = handle_swagger_request(path if path else '/')
                if swagger_response:
                    return swagger_response
            
            # Get user ID from headers
            user_id = self.auth_middleware.get_user_from_event(event)
            
            # Routes for users (admin only)
            if path == '/users' or path == '/users/':
                if method == 'GET':
                    self.auth_middleware.validate_permission(user_id, 'leitura')
                    return self.user_controller.list_users(event)
                elif method == 'POST':
                    self.auth_middleware.validate_permission(user_id, 'admin')
                    return self.user_controller.create_user(event)
            
            if path.startswith('/users/'):
                target_user_id = path.replace('/users/', '')
                if target_user_id:
                    target_user_id = unquote(target_user_id)
                    if method == 'GET':
                        self.auth_middleware.validate_permission(user_id, 'leitura')
                        return self.user_controller.get_user(event, target_user_id)
                    elif method == 'PUT':
                        self.auth_middleware.validate_permission(user_id, 'admin')
                        return self.user_controller.update_user(event, target_user_id)
                    elif method == 'DELETE':
                        self.auth_middleware.validate_permission(user_id, 'admin')
                        return self.user_controller.delete_user(event, target_user_id)
            
            # Routes for parameters
            if path == '/parameters' or path == '/parameters/':
                if method == 'GET':
                    self.auth_middleware.validate_permission(user_id, 'leitura')
                    return self.parameter_controller.list_parameters(event)
                elif method == 'POST':
                    self.auth_middleware.validate_permission(user_id, 'escrita')
                    return self.parameter_controller.create_parameter(event)
            
            # Route for listing all prefixes
            if path == '/parameters/prefixes' or path == '/parameters/prefixes/':
                if method == 'GET':
                    self.auth_middleware.validate_permission(user_id, 'leitura')
                    return self.parameter_controller.list_prefixes(event)
            
            # Route for listing parameters by prefix
            if path.startswith('/parameters/prefix/'):
                prefix = path.replace('/parameters/prefix/', '')
                if prefix and method == 'GET':
                    self.auth_middleware.validate_permission(user_id, 'leitura')
                    return self.parameter_controller.list_parameters_by_prefix(event, prefix)
            
            if path.startswith('/parameters/arn/'):
                parameter_arn = path.replace('/parameters/arn/', '')
                if parameter_arn and method == 'DELETE':
                    self.auth_middleware.validate_permission(user_id, 'admin')
                    decoded_arn = unquote(parameter_arn)
                    return self.parameter_controller.delete_parameter(event, decoded_arn)

            if path.startswith('/parameters/'):
                parameter_id = path.replace('/parameters/', '')
                if parameter_id and method in ['GET', 'PUT']:
                    decoded_id = unquote(parameter_id)
                    if '/' in decoded_id:
                        custom_prefix, param_id = decoded_id.split('/', 1)
                    else:
                        custom_prefix, param_id = '', decoded_id

                    if method == 'GET':
                        self.auth_middleware.validate_permission(user_id, 'leitura')
                        return self.parameter_controller.get_parameter(event, param_id, custom_prefix)

                    if method == 'PUT':
                        self.auth_middleware.validate_permission(user_id, 'escrita')
                        return self.parameter_controller.update_parameter(event, param_id, custom_prefix)
            
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Not found'})
            }
            
        except ValidationError as e:
            return {
                'statusCode': 403,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }
