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
    VALID_VALUE_TYPES = ['boolean', 'string', 'integer', 'double', 'date', 'time', 'datetime', 'json']
    
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
        
        # Value can be any type depending on value_type
        value = data['value']
        
        # Validate value_type if provided
        if 'value_type' in data:
            value_type = data['value_type']
            if value_type not in self.VALID_VALUE_TYPES:
                raise ValidationError(
                    f"Field 'value_type' must be one of: {', '.join(self.VALID_VALUE_TYPES)}"
                )
            
            # Validate value matches value_type
            self._validate_value_type(value, value_type)
        
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
        
        if 'domain' in data:
            domain = data['domain']
            if not isinstance(domain, str):
                raise ValidationError("Field 'domain' must be a string")
        
        if 'enabled' in data:
            enabled = data['enabled']
            if not isinstance(enabled, bool):
                raise ValidationError("Field 'enabled' must be a boolean")
        
        if 'modified_by' in data:
            modified_by = data['modified_by']
            if not isinstance(modified_by, str):
                raise ValidationError("Field 'modified_by' must be a string")
    
    def _validate_value_type(self, value: Any, value_type: str) -> None:
        """
        Validate that value matches the specified value_type
        
        Args:
            value: The value to validate
            value_type: The expected type
            
        Raises:
            ValidationError: If value doesn't match value_type
        """
        if value_type == 'boolean':
            if not isinstance(value, bool):
                raise ValidationError("Value must be a boolean when value_type is 'boolean'")
        elif value_type == 'string':
            if not isinstance(value, str):
                raise ValidationError("Value must be a string when value_type is 'string'")
        elif value_type == 'integer':
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValidationError("Value must be an integer when value_type is 'integer'")
        elif value_type == 'double':
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValidationError("Value must be a number when value_type is 'double'")
        elif value_type in ['date', 'time', 'datetime']:
            if not isinstance(value, str):
                raise ValidationError(f"Value must be a string when value_type is '{value_type}'")
        elif value_type == 'json':
            if not isinstance(value, (dict, list)):
                raise ValidationError("Value must be an object or array when value_type is 'json'")
    
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
        
        if not any(key in data for key in ['value', 'description', 'domain', 'enabled', 'value_type', 'modified_by']):
            raise ValidationError(
                "At least one of 'value', 'description', 'domain', 'enabled', 'value_type', or 'modified_by' must be provided"
            )
        
        if 'value' in data and 'value_type' in data:
            self._validate_value_type(data['value'], data['value_type'])
        
        if 'description' in data:
            description = data['description']
            if not isinstance(description, str):
                raise ValidationError("Field 'description' must be a string")
        
        if 'domain' in data:
            domain = data['domain']
            if not isinstance(domain, str):
                raise ValidationError("Field 'domain' must be a string")
        
        if 'enabled' in data:
            enabled = data['enabled']
            if not isinstance(enabled, bool):
                raise ValidationError("Field 'enabled' must be a boolean")
        
        if 'value_type' in data:
            value_type = data['value_type']
            if value_type not in self.VALID_VALUE_TYPES:
                raise ValidationError(
                    f"Field 'value_type' must be one of: {', '.join(self.VALID_VALUE_TYPES)}"
                )
        
        if 'modified_by' in data:
            modified_by = data['modified_by']
            if not isinstance(modified_by, str):
                raise ValidationError("Field 'modified_by' must be a string")
