"""
Parameter Validator following Single Responsibility Principle
"""
from typing import Dict, Any
from src.exceptions import ValidationError


class ParameterValidator:
    """
    Validates parameter inputs
    """
    
    VALID_TYPES = ['String', 'StringList', 'SecureString']
    
    def validate_create(self, data: Dict[str, Any]) -> None:
        """
        Validate data for parameter creation
        
        Args:
            data: Request body data
            
        Raises:
            ValidationError: If validation fails
        """
        if not data:
            raise ValidationError("Request body is required")
        
        if 'name' not in data:
            raise ValidationError("Field 'name' is required")
        
        if 'value' not in data:
            raise ValidationError("Field 'value' is required")
        
        name = data['name']
        if not isinstance(name, str) or not name.strip():
            raise ValidationError("Field 'name' must be a non-empty string")
        
        if '/' in name:
            raise ValidationError("Field 'name' must not contain '/' character")
        
        value = data['value']
        if not isinstance(value, str):
            raise ValidationError("Field 'value' must be a string")
        
        if 'type' in data:
            parameter_type = data['type']
            if parameter_type not in self.VALID_TYPES:
                raise ValidationError(
                    f"Field 'type' must be one of: {', '.join(self.VALID_TYPES)}"
                )
        
        if 'description' in data:
            description = data['description']
            if not isinstance(description, str):
                raise ValidationError("Field 'description' must be a string")
    
    def validate_update(self, data: Dict[str, Any]) -> None:
        """
        Validate data for parameter update
        
        Args:
            data: Request body data
            
        Raises:
            ValidationError: If validation fails
        """
        if not data:
            raise ValidationError("Request body is required")
        
        if 'value' not in data and 'description' not in data:
            raise ValidationError("At least one of 'value' or 'description' must be provided")
        
        if 'value' in data:
            value = data['value']
            if not isinstance(value, str):
                raise ValidationError("Field 'value' must be a string")
        
        if 'description' in data:
            description = data['description']
            if not isinstance(description, str):
                raise ValidationError("Field 'description' must be a string")
