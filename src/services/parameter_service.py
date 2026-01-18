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
        List all feature flag parameters
        
        Returns:
            List of parameters with their details
        """
        logger.info("Listing feature flag parameters")
        return self.repository.get_all_parameters()
    
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
        param_type: Optional[str] = None,
        last_modified_by: Optional[str] = None,
        custom_prefix: str = ''
    ) -> None:
        """
        Update an existing feature flag parameter
        
        Args:
            param_id: Parameter identifier
            value: New parameter value (optional, as string)
            description: New parameter description (optional)
            param_type: New parameter type (optional)
            last_modified_by: User who modified the parameter
            custom_prefix: Optional custom prefix within flags
        """
        logger.info(f"Updating parameter: {param_id}")
        
        if all(v is None for v in [value, description, param_type, last_modified_by]):
            logger.warning("No updates provided")
            return
        
        self.repository.update_parameter(
            param_id=param_id,
            value=value,
            description=description,
            param_type=param_type,
            last_modified_by=last_modified_by,
            custom_prefix=custom_prefix
        )
