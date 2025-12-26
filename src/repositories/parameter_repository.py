"""
Parameter Repository following Single Responsibility Principle
Data access layer for AWS Parameter Store
"""
import logging
import boto3
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
                    param_detail = {
                        'name': param['Name'].replace(f'{self.prefix}/', ''),
                        'full_name': param['Name'],
                        'type': param['Type'],
                        'last_modified': param['LastModifiedDate'].isoformat(),
                        'description': param.get('Description', '')
                    }
                    
                    try:
                        value_response = self.ssm_client.get_parameter(
                            Name=param['Name'],
                            WithDecryption=True
                        )
                        param_detail['value'] = value_response['Parameter']['Value']
                    except ClientError as e:
                        logger.warning(f"Could not retrieve value for {param['Name']}: {str(e)}")
                        param_detail['value'] = None
                    
                    parameters.append(param_detail)
            
            return parameters
            
        except ClientError as e:
            logger.error(f"Error retrieving parameters: {str(e)}")
            raise ParameterStoreError(f"Failed to list parameters: {str(e)}")
    
    def create_parameter(
        self,
        name: str,
        value: str,
        description: str = '',
        parameter_type: str = 'String'
    ) -> None:
        """
        Create a new parameter in Parameter Store
        
        Args:
            name: Full parameter name (with prefix)
            value: Parameter value
            description: Parameter description
            parameter_type: Type of parameter (String, StringList, SecureString)
        """
        try:
            self.ssm_client.put_parameter(
                Name=name,
                Value=value,
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
        value: Optional[str] = None,
        description: Optional[str] = None
    ) -> None:
        """
        Update an existing parameter
        
        Args:
            name: Full parameter name (with prefix)
            value: New parameter value (optional)
            description: New parameter description (optional)
        """
        try:
            if value is not None:
                self.ssm_client.put_parameter(
                    Name=name,
                    Value=value,
                    Overwrite=True
                )
                logger.info(f"Updated value for parameter: {name}")
            
            if description is not None:
                current_param = self.ssm_client.get_parameter(Name=name)
                self.ssm_client.put_parameter(
                    Name=name,
                    Value=current_param['Parameter']['Value'],
                    Description=description,
                    Type=current_param['Parameter']['Type'],
                    Overwrite=True
                )
                logger.info(f"Updated description for parameter: {name}")
                
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'ParameterNotFound':
                raise ParameterNotFoundError(f"Parameter {name} not found")
            logger.error(f"Error updating parameter: {str(e)}")
            raise ParameterStoreError(f"Failed to update parameter: {str(e)}")
