"""
Parameter Controller following Single Responsibility Principle
"""
import json
import logging
from typing import Dict, Any
from src.services.parameter_service import ParameterService
from src.validators.parameter_validator import ParameterValidator
from src.exceptions import ValidationError, ParameterNotFoundError

logger = logging.getLogger(__name__)


class ParameterController:
    """
    Controller for parameter operations
    """
    
    def __init__(self, service: ParameterService):
        self.service = service
        self.validator = ParameterValidator()
    
    def list_parameters(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        List all feature flag parameters
        
        Args:
            event: API Gateway event
            
        Returns:
            API Gateway response with parameter list
        """
        try:
            parameters = self.service.list_parameters()
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'parameters': parameters})
            }
        except Exception as e:
            logger.error(f"Error listing parameters: {str(e)}")
            raise
    
    def create_parameter(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new feature flag parameter
        
        Args:
            event: API Gateway event
            
        Returns:
            API Gateway response
        """
        try:
            body = json.loads(event.get('body', '{}'))
            
            self.validator.validate_create(body)
            
            name = body['name']
            value = body['value']
            description = body.get('description', '')
            domain = body.get('domain', '')
            enabled = body.get('enabled', True)
            value_type = body.get('value_type', 'string')
            modified_by = body.get('modified_by', '')
            parameter_type = body.get('type', 'String')
            
            self.service.create_parameter(
                name=name,
                value=value,
                description=description,
                domain=domain,
                enabled=enabled,
                value_type=value_type,
                modified_by=modified_by,
                parameter_type=parameter_type
            )
            
            return {
                'statusCode': 201,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'Parameter created successfully',
                    'name': f'/feature-flags/{name}',
                    'parameter': {
                        'name': name,
                        'value': value,
                        'description': description,
                        'domain': domain,
                        'enabled': enabled,
                        'value_type': value_type,
                        'modified_by': modified_by
                    }
                })
            }
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error creating parameter: {str(e)}")
            raise
    
    def update_parameter(self, event: Dict[str, Any], parameter_name: str) -> Dict[str, Any]:
        """
        Update an existing feature flag parameter
        
        Args:
            event: API Gateway event
            parameter_name: Name of parameter to update
            
        Returns:
            API Gateway response
        """
        try:
            body = json.loads(event.get('body', '{}'))
            
            self.validator.validate_update(body)
            
            value = body.get('value')
            description = body.get('description')
            domain = body.get('domain')
            enabled = body.get('enabled')
            value_type = body.get('value_type')
            modified_by = body.get('modified_by')
            
            self.service.update_parameter(
                name=parameter_name,
                value=value,
                description=description,
                domain=domain,
                enabled=enabled,
                value_type=value_type,
                modified_by=modified_by
            )
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'Parameter updated successfully',
                    'name': f'/feature-flags/{parameter_name}'
                })
            }
        except ValidationError:
            raise
        except ParameterNotFoundError as e:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }
        except Exception as e:
            logger.error(f"Error updating parameter: {str(e)}")
            raise
