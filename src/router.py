"""
Router for API endpoints
"""
import json
import logging
from typing import Dict, Any
from src.controllers.parameter_controller import ParameterController
from src.services.parameter_service import ParameterService

logger = logging.getLogger(__name__)


class Router:
    """
    Routes HTTP requests to appropriate controllers
    """
    
    def __init__(self, service: ParameterService):
        self.controller = ParameterController(service)
    
    def route(self, method: str, path: str, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route request to appropriate controller method
        
        Args:
            method: HTTP method
            path: Request path
            event: Complete API Gateway event
            
        Returns:
            API Gateway response
        """
        if path == '/parameters' or path == '/parameters/':
            if method == 'GET':
                return self.controller.list_parameters(event)
            elif method == 'POST':
                return self.controller.create_parameter(event)
        
        if path.startswith('/parameters/'):
            parameter_name = path.replace('/parameters/', '')
            if parameter_name and method == 'PUT':
                return self.controller.update_parameter(event, parameter_name)
        
        return {
            'statusCode': 404,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Not found'})
        }
