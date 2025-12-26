"""
Integration tests for Lambda handler
"""
import json
import pytest
from unittest.mock import Mock, patch
from lambda_function import lambda_handler


class TestLambdaHandler:
    """Test cases for Lambda handler"""
    
    @patch('lambda_function.APIHandler')
    def test_handler_success(self, mock_handler_class):
        """Test successful Lambda invocation"""
        mock_handler = Mock()
        mock_handler.handle.return_value = {
            'statusCode': 200,
            'body': json.dumps({'parameters': []})
        }
        mock_handler_class.return_value = mock_handler
        
        event = {
            'httpMethod': 'GET',
            'path': '/parameters'
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        mock_handler.handle.assert_called_once_with(event, context)
    
    @patch('lambda_function.APIHandler')
    def test_handler_validation_error(self, mock_handler_class):
        """Test Lambda handler with validation error"""
        from src.exceptions import ValidationError
        
        mock_handler = Mock()
        mock_handler.handle.side_effect = ValidationError("Invalid input")
        mock_handler_class.return_value = mock_handler
        
        event = {
            'httpMethod': 'POST',
            'path': '/parameters',
            'body': json.dumps({})
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'error' in body
    
    @patch('lambda_function.APIHandler')
    def test_handler_unexpected_error(self, mock_handler_class):
        """Test Lambda handler with unexpected error"""
        mock_handler = Mock()
        mock_handler.handle.side_effect = Exception("Unexpected error")
        mock_handler_class.return_value = mock_handler
        
        event = {
            'httpMethod': 'GET',
            'path': '/parameters'
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 500
        body = json.loads(response['body'])
        assert body['error'] == 'Internal server error'
