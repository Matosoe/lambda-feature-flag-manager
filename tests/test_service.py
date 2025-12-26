"""
Unit tests for Parameter Service
"""
import pytest
from unittest.mock import Mock, MagicMock
from src.services.parameter_service import ParameterService


class TestParameterService:
    """Test cases for ParameterService"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.mock_repository = Mock()
        self.service = ParameterService(self.mock_repository)
    
    def test_list_parameters(self):
        """Test listing parameters"""
        expected_params = [
            {'name': 'feature1', 'value': 'enabled'},
            {'name': 'feature2', 'value': 'disabled'}
        ]
        self.mock_repository.get_all_parameters.return_value = expected_params
        
        result = self.service.list_parameters()
        
        assert result == expected_params
        self.mock_repository.get_all_parameters.assert_called_once()
    
    def test_create_parameter(self):
        """Test creating a parameter"""
        self.service.create_parameter(
            name='test-feature',
            value='enabled',
            description='Test',
            parameter_type='String'
        )
        
        self.mock_repository.create_parameter.assert_called_once_with(
            name='/feature-flags/test-feature',
            value='enabled',
            description='Test',
            parameter_type='String'
        )
    
    def test_update_parameter_with_value(self):
        """Test updating parameter value"""
        self.service.update_parameter(
            name='test-feature',
            value='disabled'
        )
        
        self.mock_repository.update_parameter.assert_called_once_with(
            name='/feature-flags/test-feature',
            value='disabled',
            description=None
        )
    
    def test_update_parameter_with_description(self):
        """Test updating parameter description"""
        self.service.update_parameter(
            name='test-feature',
            description='New description'
        )
        
        self.mock_repository.update_parameter.assert_called_once_with(
            name='/feature-flags/test-feature',
            value=None,
            description='New description'
        )
    
    def test_update_parameter_no_changes(self):
        """Test update with no changes does nothing"""
        self.service.update_parameter(name='test-feature')
        
        self.mock_repository.update_parameter.assert_not_called()
