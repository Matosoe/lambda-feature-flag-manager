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
        value: str,
        description: str = '',
        parameter_type: str = 'String'
    ) -> None:
        """
        Create a new feature flag parameter
        
        Args:
            name: Parameter name (will be prefixed with /feature-flags/)
            value: Parameter value
            description: Parameter description
            parameter_type: Parameter type (String, StringList, SecureString)
        """
        full_name = f'/feature-flags/{name}'
        logger.info(f"Creating parameter: {full_name}")
        
        self.repository.create_parameter(
            name=full_name,
            value=value,
            description=description,
            parameter_type=parameter_type
        )
    
    def update_parameter(
        self,
        name: str,
        value: Optional[str] = None,
        description: Optional[str] = None
    ) -> None:
        """
        Update an existing feature flag parameter
        
        Args:
            name: Parameter name (without /feature-flags/ prefix)
            value: New parameter value (optional)
            description: New parameter description (optional)
        """
        full_name = f'/feature-flags/{name}'
        logger.info(f"Updating parameter: {full_name}")
        
        if value is None and description is None:
            logger.warning("No updates provided")
            return
        
        self.repository.update_parameter(
            name=full_name,
            value=value,
            description=description
        )
