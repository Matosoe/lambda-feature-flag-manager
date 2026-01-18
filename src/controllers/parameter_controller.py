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
        List all feature flag parameters with hierarchical organization
        
        Args:
            event: API Gateway event
            
        Returns:
            API Gateway response with parameter list including path and ARN
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
    
    def list_parameters_by_prefix(self, event: Dict[str, Any], prefix: str) -> Dict[str, Any]:
        """
        List feature flag parameters filtered by prefix
        
        Args:
            event: API Gateway event
            prefix: Custom prefix to filter by
            
        Returns:
            API Gateway response with filtered parameter list
        """
        try:
            parameters = self.service.list_parameters_by_prefix(prefix)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'prefix': prefix,
                    'parameters': parameters
                })
            }
        except Exception as e:
            logger.error(f"Error listing parameters by prefix: {str(e)}")
            raise

    def get_parameter(self, event: Dict[str, Any], parameter_id: str, custom_prefix: str = '') -> Dict[str, Any]:
        """
        Get a specific feature flag parameter

        Args:
            event: API Gateway event
            parameter_id: ID of parameter
            custom_prefix: Optional custom prefix

        Returns:
            API Gateway response
        """
        try:
            parameter = self.service.get_parameter(param_id=parameter_id, custom_prefix=custom_prefix)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(parameter)
            }
        except ParameterNotFoundError as e:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }
        except Exception as e:
            logger.error(f"Error getting parameter: {str(e)}")
            raise
    
    def list_prefixes(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        List all available prefixes
        
        Args:
            event: API Gateway event
            
        Returns:
            API Gateway response with list of prefixes
        """
        try:
            logger.info("Listing all available prefixes")
            prefixes = self.service.list_prefixes()
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'prefixes': prefixes
                })
            }
        except Exception as e:
            logger.error(f"Error listing prefixes: {str(e)}")
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
            try:
                body = json.loads(event.get('body', '{}'))
            except json.JSONDecodeError as e:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': f'Invalid JSON body: {str(e)}'})
                }
            
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
    
    def update_parameter(self, event: Dict[str, Any], parameter_id: str, custom_prefix: str = '') -> Dict[str, Any]:
        """
        Update an existing feature flag parameter
        
        Args:
            event: API Gateway event
            parameter_id: ID of parameter to update
            
        Returns:
            API Gateway response
        """
        try:
            try:
                body = json.loads(event.get('body', '{}'))
            except json.JSONDecodeError as e:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': f'Invalid JSON body: {str(e)}'})
                }
            
            self.validator.validate_update(body)
            
            value = body.get('value')
            description = body.get('description')
            last_modified_by = event.get('headers', {}).get('X-User-Id', '')
            
            self.service.update_parameter(
                param_id=parameter_id,
                value=value,
                description=description,
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

    def delete_parameter(self, event: Dict[str, Any], parameter_arn: str) -> Dict[str, Any]:
        """
        Delete an existing feature flag parameter using ARN

        Args:
            event: API Gateway event
            parameter_arn: ARN of parameter to delete

        Returns:
            API Gateway response
        """
        try:
            required_prefix = ":parameter/feature-flags/flags"
            if required_prefix not in parameter_arn:
                raise ValidationError(
                    "Parameter ARN must contain ':parameter/feature-flags/flags'"
                )

            self.service.delete_parameter_by_arn(parameter_arn)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'Parameter deleted successfully',
                    'arn': parameter_arn
                })
            }
        except ParameterNotFoundError as e:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }
        except Exception as e:
            logger.error(f"Error deleting parameter: {str(e)}")
            raise
