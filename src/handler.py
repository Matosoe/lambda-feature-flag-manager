"""
API Handler following Single Responsibility Principle
"""
import json
import logging
from typing import Dict, Any
from src.router import Router
from src.services.parameter_service import ParameterService
from src.repositories.parameter_repository import ParameterRepository

logger = logging.getLogger(__name__)


class APIHandler:
    """
    Handles API Gateway events and routes to appropriate controllers
    """
    
    def __init__(self):
        repository = ParameterRepository()
        service = ParameterService(repository)
        self.router = Router(service)
    
    def handle(self, event: Dict[str, Any], context: Any) -> Dict[str, Any]:
        """
        Process API Gateway event
        
        Args:
            event: API Gateway event
            context: Lambda context
            
        Returns:
            API Gateway response
        """
        logger.info(f"Received event: {json.dumps(event)}")
        
        http_method = event.get('httpMethod', '')
        path = event.get('path', '')
        
        response = self.router.route(http_method, path, event)
        
        logger.info(f"Response status: {response.get('statusCode')}")
        return response
