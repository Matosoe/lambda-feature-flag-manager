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
            
            param_id = body['id']
            value = body['value']
            param_type = body['type']
            description = body.get('description', '')
            last_modified_by = body.get('lastModifiedBy', '')
            parameter_store_type = body.get('parameterStoreType', 'String')
            custom_prefix = body.get('prefix', '')  # Optional custom prefix
            
            self.service.create_parameter(
                param_id=param_id,
                value=value,
                param_type=param_type,
                description=description,
                last_modified_by=last_modified_by,
                parameter_store_type=parameter_store_type,
                custom_prefix=custom_prefix
            )
            
            return {
                'statusCode': 201,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'Parameter created successfully',
                    'id': param_id,
                    'parameter': {
                        'id': param_id,
                        'value': value,
                        'type': param_type,
                        'description': description,
                        'lastModifiedBy': last_modified_by
                    }
                })
            }
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error creating parameter: {str(e)}")
            raise
    
    def update_parameter(self, event: Dict[str, Any], parameter_id: str) -> Dict[str, Any]:
        """
        Update an existing feature flag parameter
        
        Args:
            event: API Gateway event
            parameter_id: ID of parameter to update
            
        Returns:
            API Gateway response
        """
        try:
            body = json.loads(event.get('body', '{}'))
            
            self.validator.validate_update(body)
            
            value = body.get('value')
            description = body.get('description')
            param_type = body.get('type')
            last_modified_by = body.get('lastModifiedBy')
            custom_prefix = body.get('prefix', '')  # Optional custom prefix
            
            self.service.update_parameter(
                param_id=parameter_id,
                value=value,
                description=description,
                param_type=param_type,
                last_modified_by=last_modified_by,
                custom_prefix=custom_prefix
            )
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'Parameter updated successfully',
                    'id': parameter_id
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
