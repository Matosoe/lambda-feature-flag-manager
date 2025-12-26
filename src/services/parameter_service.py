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
        Create a new feature flag parameter with complete metadata
        
        Args:
            name: Parameter name (will be prefixed with /feature-flags/)
            value: Parameter value (any type based on value_type)
            description: Parameter description
            domain: Parameter domain
            enabled: Whether the flag is enabled
            value_type: Type of the value (boolean, string, integer, double, date, time, datetime, json)
            modified_by: User who created the parameter
            parameter_type: AWS Parameter type (String, StringList, SecureString)
        """
        full_name = f'/feature-flags/{name}'
        logger.info(f"Creating parameter: {full_name}")
        
        self.repository.create_parameter(
            name=full_name,
            value=value,
            description=description,
            domain=domain,
            enabled=enabled,
            value_type=value_type,
            modified_by=modified_by,
            parameter_type=parameter_type
        )
    
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
        Update an existing feature flag parameter
        
        Args:
            name: Parameter name (without /feature-flags/ prefix)
            value: New parameter value (optional)
            description: New parameter description (optional)
            domain: New parameter domain (optional)
            enabled: New enabled status (optional)
            value_type: New value type (optional)
            modified_by: User who modified the parameter
        """
        full_name = f'/feature-flags/{name}'
        logger.info(f"Updating parameter: {full_name}")
        
        if all(v is None for v in [value, description, domain, enabled, value_type, modified_by]):
            logger.warning("No updates provided")
            return
        
        self.repository.update_parameter(
            name=full_name,
            value=value,
            description=description,
            domain=domain,
            enabled=enabled,
            value_type=value_type,
            modified_by=modified_by
        )
