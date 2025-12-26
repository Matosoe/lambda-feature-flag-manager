"""
Parameter Repository following Single Responsibility Principle
Data access layer for AWS Parameter Store
"""
import logging
import boto3import json
from datetime import datetimefrom typing import List, Dict, Any, Optional
from botocore.exceptions import ClientError
from src.exceptions import ParameterStoreError, ParameterNotFoundError

logger = logging.getLogger(__name__)


class ParameterRepository:
    """
    Repository for AWS Systems Manager Parameter Store operations
    Follows Interface Segregation and Dependency Inversion principles
    """
    
    def __init__(self):
        self.ssm_client = boto3.client('ssm')
        self.prefix = '/feature-flags'
    
    def get_all_parameters(self) -> List[Dict[str, Any]]:
        """
        Retrieve all parameters with /feature-flags prefix
        
        Returns:
            List of parameter dictionaries
        """
        try:
            parameters = []
            paginator = self.ssm_client.get_paginator('describe_parameters')
            
            page_iterator = paginator.paginate(
                ParameterFilters=[
                    {
                        'Key': 'Name',
                        'Option': 'BeginsWith',
                        'Values': [self.prefix]
                    }
                ]
            )
            
            for page in page_iterator:
                for param in page.get('Parameters', []):
                    try:
                        value_response = self.ssm_client.get_parameter(
                            Name=param['Name'],
                            WithDecryption=True
                        )
                        param_value = value_response['Parameter']['Value']
                        
                        # Parse the JSON structure
                        try:
                            param_data = json.loads(param_value)
                            param_detail = {
                                'name': param['Name'].replace(f'{self.prefix}/', ''),
                                'full_name': param['Name'],
                                'description': param_data.get('description', ''),
                                'domain': param_data.get('domain', ''),
                                'last_modified': param_data.get('last_modified', param['LastModifiedDate'].isoformat()),
                                'modified_by': param_data.get('modified_by', ''),
                                'enabled': param_data.get('enabled', True),
                                'value_type': param_data.get('value_type', 'string'),
                                'value': param_data.get('value')
                            }
                        except (json.JSONDecodeError, TypeError):
                            # Fallback for old format parameters
                            param_detail = {
                                'name': param['Name'].replace(f'{self.prefix}/', ''),
                                'full_name': param['Name'],
                                'description': param.get('Description', ''),
                                'domain': '',
                                'last_modified': param['LastModifiedDate'].isoformat(),
                                'modified_by': '',
                                'enabled': True,
                                'value_type': 'string',
                                'value': param_value
                            }
                    except ClientError as e:
                        logger.warning(f"Could not retrieve value for {param['Name']}: {str(e)}")
                        param_detail = {
                            'name': param['Name'].replace(f'{self.prefix}/', ''),
                            'full_name': param['Name'],
                            'description': param.get('Description', ''),
                            'domain': '',
                            'last_modified': param['LastModifiedDate'].isoformat(),
                            'modified_by': '',
                            'enabled': False,
                            'value_type': 'string',
                            'value': None
                        }
                    
                    parameters.append(param_detail)
            
            return parameters
            
        except ClientError as e:
            logger.error(f"Error retrieving parameters: {str(e)}")
            raise ParameterStoreError(f"Failed to list parameters: {str(e)}")
    
    def create_parameter(
        self,
        name: str,
        value: Any,
        description: str = '',
        domain: str = '',
        enabled: bool = True,
        value_type: str = 'string',
        modified_by: str = '',
        parameter_type: str = 'String'
    ) -> None:
        """
        Create a new parameter in Parameter Store with structured JSON format
        
        Args:
            name: Full parameter name (with prefix)
            value: Parameter value
            description: Parameter description
            domain: Parameter domain
            enabled: Whether the flag is enabled
            value_type: Type of the value (boolean, string, integer, double, date, time, json)
            modified_by: User who created the parameter
            parameter_type: AWS Parameter type (String, StringList, SecureString)
        """
        try:
            # Create structured JSON value
            param_data = {
                'description': description,
                'domain': domain,
                'last_modified': datetime.utcnow().isoformat(),
                'modified_by': modified_by,
                'enabled': enabled,
                'value_type': value_type,
                'value': value
            }
            
            json_value = json.dumps(param_data)
            
            self.ssm_client.put_parameter(
                Name=name,
                Value=json_value,
                Description=description,
                Type=parameter_type,
                Overwrite=False
            )
            logger.info(f"Successfully created parameter: {name}")
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'ParameterAlreadyExists':
                raise ParameterStoreError(f"Parameter {name} already exists")
            logger.error(f"Error creating parameter: {str(e)}")
            raise ParameterStoreError(f"Failed to create parameter: {str(e)}")
    
    def update_parameter(
        self,
        name: str,
        value: Optional[Any] = None,
        description: Optional[str] = None,
        domain: Optional[str] = None,
        enabled: Optional[bool] = None,
        value_type: Optional[str] = None,
        modified_by: Optional[str] = None
    ) -> None:
        """
        Update an existing parameter maintaining JSON structure
        
        Args:
            name: Full parameter name (with prefix)
            value: New parameter value (optional)
            description: New parameter description (optional)
            domain: New parameter domain (optional)
            enabled: New enabled status (optional)
            value_type: New value type (optional)
            modified_by: User who modified the parameter
        """
        try:
            # Get current parameter
            current_param = self.ssm_client.get_parameter(Name=name, WithDecryption=True)
            current_value = current_param['Parameter']['Value']
            
            # Try to parse existing JSON structure
            try:
                param_data = json.loads(current_value)
            except (json.JSONDecodeError, TypeError):
                # If not JSON, create new structure with current value
                param_data = {
                    'description': description or '',
                    'domain': domain or '',
                    'last_modified': datetime.utcnow().isoformat(),
                    'modified_by': modified_by or '',
                    'enabled': enabled if enabled is not None else True,
                    'value_type': value_type or 'string',
                    'value': value if value is not None else current_value
                }
            else:
                # Update only provided fields
                if value is not None:
                    param_data['value'] = value
                if description is not None:
                    param_data['description'] = description
                if domain is not None:
                    param_data['domain'] = domain
                if enabled is not None:
                    param_data['enabled'] = enabled
                if value_type is not None:
                    param_data['value_type'] = value_type
                if modified_by is not None:
                    param_data['modified_by'] = modified_by
                
                param_data['last_modified'] = datetime.utcnow().isoformat()
            
            json_value = json.dumps(param_data)
            
            self.ssm_client.put_parameter(
                Name=name,
                Value=json_value,
                Description=param_data.get('description', ''),
                Type=current_param['Parameter']['Type'],
                Overwrite=True
            )
            logger.info(f"Updated parameter: {name}")
                
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'ParameterNotFound':
                raise ParameterNotFoundError(f"Parameter {name} not found")
            logger.error(f"Error updating parameter: {str(e)}")
            raise ParameterStoreError(f"Failed to update parameter: {str(e)}")
