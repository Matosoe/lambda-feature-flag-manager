"""
Parameter Service following Single Responsibility Principle
Business logic layer
"""
import logging
from typing import List, Dict, Any, Optional
from src.repositories.parameter_repository import ParameterRepository

logger = logging.getLogger(__name__)


class ParameterService:
    """
    Service for managing feature flag parameters
    Contains business logic
    """
    
    def __init__(self, repository: ParameterRepository):
        self.repository = repository
    
    def list_parameters(self) -> List[Dict[str, Any]]:
        """
        List all feature flag parameters organized by prefix hierarchy
        
        Returns:
            List of parameters with their details including path and ARN
        """
        logger.info("Listing feature flag parameters")
        parameters = self.repository.get_all_parameters()
        
        # Sort by ARN to maintain hierarchical order
        parameters.sort(key=lambda x: x.get('arn', ''))
        
        return parameters
    
    def list_parameters_by_prefix(self, prefix: str) -> List[Dict[str, Any]]:
        """
        List feature flag parameters filtered by custom prefix
        
        Args:
            prefix: Custom prefix within /feature-flags/flags (e.g., 'ui', 'api', 'config')
            
        Returns:
            List of parameters matching the prefix
        """
        logger.info(f"Listing feature flag parameters with prefix: {prefix}")
        parameters = self.repository.get_parameters_by_prefix(prefix)
        
        # Sort by ARN to maintain hierarchical order
        parameters.sort(key=lambda x: x.get('arn', ''))
        
        return parameters
    
    def list_prefixes(self) -> List[str]:
        """
        List all available prefixes under /feature-flags/flags/
        
        Returns:
            List of unique prefix strings sorted alphabetically
        """
        return self.repository.get_all_prefixes()
    
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
        Create a new feature flag parameter with complete metadata
        
        Args:
            param_id: Parameter identifier
            value: Parameter value (as string)
            param_type: Type of the value (BOOLEAN, STRING, INTEGER, DOUBLE, DATE, TIME, DATETIME, JSON)
            description: Parameter description
            last_modified_by: User who created the parameter
            parameter_store_type: AWS Parameter type (String, StringList, SecureString)
            custom_prefix: Optional custom prefix within flags
        """
        logger.info(f"Creating parameter: {param_id}")
        
        self.repository.create_parameter(
            param_id=param_id,
            value=value,
            param_type=param_type,
            description=description,
            last_modified_by=last_modified_by,
            parameter_store_type=parameter_store_type,
            custom_prefix=custom_prefix
        )
    
    def update_parameter(
        self,
        param_id: str,
        value: Optional[str] = None,
        description: Optional[str] = None,
        last_modified_by: Optional[str] = None,
        custom_prefix: str = ''
    ) -> None:
        """
        Update an existing feature flag parameter
        
        Args:
            param_id: Parameter identifier
            value: New parameter value (optional, as string)
            description: New parameter description (optional)
            custom_prefix: Optional custom prefix within flags
        """
        logger.info(f"Updating parameter: {param_id}")
        
        if all(v is None for v in [value, description]):
            logger.warning("No updates provided")
            return
        
        self.repository.update_parameter(
            param_id=param_id,
            value=value,
            description=description,
            last_modified_by=last_modified_by,
            custom_prefix=custom_prefix
        )

    def delete_parameter(self, param_id: str, custom_prefix: str = '') -> None:
        """
        Delete an existing feature flag parameter

        Args:
            param_id: Parameter identifier
            custom_prefix: Optional custom prefix within flags
        """
        logger.info(f"Deleting parameter: {param_id}")
        self.repository.delete_parameter(param_id=param_id, custom_prefix=custom_prefix)

    def delete_parameter_by_arn(self, arn: str) -> None:
        """
        Delete a parameter using its ARN

        Args:
            arn: Parameter ARN
        """
        logger.info(f"Deleting parameter by ARN: {arn}")
        # Extract full parameter path from ARN
        full_name = arn.split(':parameter', 1)[-1]
        self.repository.delete_parameter_by_path(full_name)
