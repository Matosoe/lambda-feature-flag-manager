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
    VALID_PARAM_TYPES = ['BOOLEAN', 'STRING', 'INTEGER', 'DOUBLE', 'DATE', 'TIME', 'DATETIME', 'JSON']
    
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
        
        if 'id' not in data:
            raise ValidationError("Field 'id' is required")
        
        if 'value' not in data:
            raise ValidationError("Field 'value' is required")
        
        if 'type' not in data:
            raise ValidationError("Field 'type' is required")
        
        param_id = data['id']
        if not isinstance(param_id, str) or not param_id.strip():
            raise ValidationError("Field 'id' must be a non-empty string")
        
        # Value must be a string
        value = data['value']
        if not isinstance(value, str):
            raise ValidationError("Field 'value' must be a string")
        
        # Validate type
        param_type = data['type']
        if param_type not in self.VALID_PARAM_TYPES:
            raise ValidationError(
                f"Field 'type' must be one of: {', '.join(self.VALID_PARAM_TYPES)}"
            )
        
        if 'parameterStoreType' in data:
            parameter_type = data['parameterStoreType']
            if parameter_type not in self.VALID_TYPES:
                raise ValidationError(
                    f"Field 'parameterStoreType' must be one of: {', '.join(self.VALID_TYPES)}"
                )
        
        if 'description' in data:
            description = data['description']
            if not isinstance(description, str):
                raise ValidationError("Field 'description' must be a string")
        
        if 'lastModifiedBy' in data:
            last_modified_by = data['lastModifiedBy']
            if not isinstance(last_modified_by, str):
                raise ValidationError("Field 'lastModifiedBy' must be a string")
    
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
        
        if not any(key in data for key in ['value', 'description', 'type', 'lastModifiedBy']):
            raise ValidationError(
                "At least one of 'value', 'description', 'type', or 'lastModifiedBy' must be provided"
            )
        
        if 'value' in data:
            value = data['value']
            if not isinstance(value, str):
                raise ValidationError("Field 'value' must be a string")
        
        if 'description' in data:
            description = data['description']
            if not isinstance(description, str):
                raise ValidationError("Field 'description' must be a string")
        
        if 'type' in data:
            param_type = data['type']
            if param_type not in self.VALID_PARAM_TYPES:
                raise ValidationError(
                    f"Field 'type' must be one of: {', '.join(self.VALID_PARAM_TYPES)}"
                )
        
        if 'lastModifiedBy' in data:
            last_modified_by = data['lastModifiedBy']
            if not isinstance(last_modified_by, str):
                raise ValidationError("Field 'lastModifiedBy' must be a string")
