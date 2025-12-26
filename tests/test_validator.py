"""
Unit tests for Parameter Validator
"""
import pytest
from src.validators.parameter_validator import ParameterValidator
from src.exceptions import ValidationError


class TestParameterValidator:
    """Test cases for ParameterValidator"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.validator = ParameterValidator()
    
    def test_validate_create_success(self):
        """Test successful validation for create"""
        data = {
            'name': 'test-feature',
            'value': 'enabled',
            'description': 'Test feature',
            'type': 'String'
        }
        self.validator.validate_create(data)
    
    def test_validate_create_missing_name(self):
        """Test validation fails when name is missing"""
        data = {'value': 'enabled'}
        with pytest.raises(ValidationError, match="Field 'name' is required"):
            self.validator.validate_create(data)
    
    def test_validate_create_missing_value(self):
        """Test validation fails when value is missing"""
        data = {'name': 'test-feature'}
        with pytest.raises(ValidationError, match="Field 'value' is required"):
            self.validator.validate_create(data)
    
    def test_validate_create_empty_name(self):
        """Test validation fails when name is empty"""
        data = {'name': '', 'value': 'enabled'}
        with pytest.raises(ValidationError, match="must be a non-empty string"):
            self.validator.validate_create(data)
    
    def test_validate_create_name_with_slash(self):
        """Test validation fails when name contains slash"""
        data = {'name': 'test/feature', 'value': 'enabled'}
        with pytest.raises(ValidationError, match="must not contain '/' character"):
            self.validator.validate_create(data)
    
    def test_validate_create_invalid_type(self):
        """Test validation fails with invalid parameter type"""
        data = {'name': 'test', 'value': 'enabled', 'type': 'InvalidType'}
        with pytest.raises(ValidationError, match="must be one of"):
            self.validator.validate_create(data)
    
    def test_validate_update_success(self):
        """Test successful validation for update"""
        data = {'value': 'disabled'}
        self.validator.validate_update(data)
    
    def test_validate_update_no_fields(self):
        """Test validation fails when no fields provided"""
        data = {}
        with pytest.raises(ValidationError, match="At least one of"):
            self.validator.validate_update(data)
    
    def test_validate_update_invalid_value_type(self):
        """Test validation fails when value is not string"""
        data = {'value': 123}
        with pytest.raises(ValidationError, match="must be a string"):
            self.validator.validate_update(data)
