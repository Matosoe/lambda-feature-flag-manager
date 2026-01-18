"""
Parameter Repository following Single Responsibility Principle
Data access layer for AWS Parameter Store
"""
import logging
import boto3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
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
        self.prefix = '/feature-flags/flags'
        self.users_path = '/feature-flags/users'
    
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
                                'id': param_data.get('id', param['Name'].replace(f'{self.prefix}/', '')),
                                'value': param_data.get('value', ''),
                                'type': param_data.get('type', 'STRING'),
                                'description': param_data.get('description', ''),
                                'lastModifiedAt': param_data.get('lastModifiedAt', param['LastModifiedDate'].isoformat()),
                                'lastModifiedBy': param_data.get('lastModifiedBy', '')
                            }
                            # Include previousVersion if present
                            if 'previousVersion' in param_data:
                                param_detail['previousVersion'] = param_data['previousVersion']
                        except (json.JSONDecodeError, TypeError):
                            # Fallback for old format parameters
                            param_detail = {
                                'id': param['Name'].replace(f'{self.prefix}/', ''),
                                'value': param_value,
                                'type': 'STRING',
                                'description': param.get('Description', ''),
                                'lastModifiedAt': param['LastModifiedDate'].isoformat(),
                                'lastModifiedBy': ''
                            }
                    except ClientError as e:
                        logger.warning(f"Could not retrieve value for {param['Name']}: {str(e)}")
                        param_detail = {
                            'id': param['Name'].replace(f'{self.prefix}/', ''),
                            'value': '',
                            'type': 'STRING',
                            'description': param.get('Description', ''),
                            'lastModifiedAt': param['LastModifiedDate'].isoformat(),
                            'lastModifiedBy': ''
                        }
                    
                    parameters.append(param_detail)
            
            return parameters
            
        except ClientError as e:
            logger.error(f"Error retrieving parameters: {str(e)}")
            raise ParameterStoreError(f"Failed to list parameters: {str(e)}")
    
    def create_parameter(
        self,
        param_id: str,
        value: str,
        param_type: str = 'STRING',
        description: str = '',
        last_modified_by: str = '',
        parameter_store_type: str = 'String',
        custom_prefix: str = ''
    ) -> None:
        """
        Create a new parameter in Parameter Store with structured JSON format
        
        Args:
            param_id: Parameter identifier (used as name)
            value: Parameter value (as string)
            param_type: Type of the value (BOOLEAN, STRING, INTEGER, DOUBLE, DATE, TIME, DATETIME, JSON)
            description: Parameter description
            last_modified_by: User who created the parameter
            parameter_store_type: AWS Parameter type (String, StringList, SecureString)
            custom_prefix: Optional custom prefix within flags (e.g., 'api', 'ui')
        """
        try:
            # Create structured JSON value
            param_data = {
                'id': param_id,
                'value': value,
                'type': param_type,
                'description': description,
                'lastModifiedAt': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                'lastModifiedBy': last_modified_by
            }
            
            json_value = json.dumps(param_data)
            
            # Build full name with custom prefix if provided
            if custom_prefix:
                full_name = f'{self.prefix}/{custom_prefix}/{param_id}'
            else:
                full_name = f'{self.prefix}/{param_id}'
            
            self.ssm_client.put_parameter(
                Name=full_name,
                Value=json_value,
                Description=description,
                Type=parameter_store_type,
                Overwrite=False
            )
            logger.info(f"Successfully created parameter: {full_name}")
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'ParameterAlreadyExists':
                raise ParameterStoreError(f"Parameter {param_id} already exists")
            logger.error(f"Error creating parameter: {str(e)}")
            raise ParameterStoreError(f"Failed to create parameter: {str(e)}")
    
    def update_parameter(
        self,
        param_id: str,
        value: Optional[str] = None,
        description: Optional[str] = None,
        param_type: Optional[str] = None,
        last_modified_by: Optional[str] = None,
        custom_prefix: str = ''
    ) -> None:
        """
        Update an existing parameter maintaining JSON structure and keeping previous version
        
        Args:
            param_id: Parameter identifier
            value: New parameter value (optional, as string)
            description: New parameter description (optional)
            param_type: New parameter type (optional)
            last_modified_by: User who modified the parameter
            custom_prefix: Optional custom prefix within flags
        """
        try:
            # Build full parameter name
            if custom_prefix:
                full_name = f'{self.prefix}/{custom_prefix}/{param_id}'
            else:
                full_name = f'{self.prefix}/{param_id}'
            
            # Get current parameter
            current_param = self.ssm_client.get_parameter(Name=full_name, WithDecryption=True)
            current_value = current_param['Parameter']['Value']
            
            # Try to parse existing JSON structure
            try:
                param_data = json.loads(current_value)
            except (json.JSONDecodeError, TypeError):
                # If not JSON, create new structure with current value
                param_data = {
                    'id': param_id,
                    'value': value if value is not None else current_value,
                    'type': param_type or 'STRING',
                    'description': description or '',
                    'lastModifiedAt': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'lastModifiedBy': last_modified_by or ''
                }
            else:
                # Save current version as previousVersion before updating
                if value is not None and value != param_data.get('value'):
                    param_data['previousVersion'] = {
                        'value': param_data.get('value', ''),
                        'modifiedAt': param_data.get('lastModifiedAt', ''),
                        'modifiedBy': param_data.get('lastModifiedBy', '')
                    }
                
                # Update only provided fields
                if value is not None:
                    param_data['value'] = value
                if description is not None:
                    param_data['description'] = description
                if param_type is not None:
                    param_data['type'] = param_type
                if last_modified_by is not None:
                    param_data['lastModifiedBy'] = last_modified_by
                
                param_data['lastModifiedAt'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            
            json_value = json.dumps(param_data)
            
            self.ssm_client.put_parameter(
                Name=full_name,
                Value=json_value,
                Description=param_data.get('description', ''),
                Type=current_param['Parameter']['Type'],
                Overwrite=True
            )
            logger.info(f"Updated parameter: {full_name}")
                
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'ParameterNotFound':
                raise ParameterNotFoundError(f"Parameter {param_id} not found")
            logger.error(f"Error updating parameter: {str(e)}")
            raise ParameterStoreError(f"Failed to update parameter: {str(e)}")
