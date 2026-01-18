"""
User Controller for HTTP request/response handling
"""
import json
import logging
from typing import Dict, Any
from src.services.user_service import UserService
from src.exceptions import ValidationError, ParameterNotFoundError

logger = logging.getLogger(__name__)


class UserController:
    """
    Controller for user operations
    """
    
    def __init__(self, service: UserService):
        self.service = service
    
    def list_users(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        List all users
        
        Args:
            event: API Gateway event
            
        Returns:
            API Gateway response with user list
        """
        try:
            users = self.service.list_users()
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'usuarios': users}, ensure_ascii=False)
            }
        except Exception as e:
            logger.error(f"Error listing users: {str(e)}")
            raise
    
    def get_user(self, event: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Get a specific user
        
        Args:
            event: API Gateway event
            user_id: User email/identifier
            
        Returns:
            API Gateway response
        """
        try:
            user = self.service.get_user(user_id)
            
            if not user:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': f'User {user_id} not found'})
                }
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(user, ensure_ascii=False)
            }
        except Exception as e:
            logger.error(f"Error getting user: {str(e)}")
            raise
    
    def create_user(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user
        
        Args:
            event: API Gateway event
            
        Returns:
            API Gateway response
        """
        try:
            body = json.loads(event.get('body', '{}'))
            
            # Validate required fields
            if 'id' not in body:
                raise ValidationError("Field 'id' is required")
            if 'nome' not in body:
                raise ValidationError("Field 'nome' is required")
            if 'permissoes' not in body:
                raise ValidationError("Field 'permissoes' is required")
            
            user_id = body['id']
            nome = body['nome']
            permissoes = body['permissoes']
            ativo = body.get('ativo', True)
            
            # Validate permissoes structure
            if not isinstance(permissoes, dict):
                raise ValidationError("Field 'permissoes' must be an object")
            
            required_perms = ['leitura', 'escrita', 'admin']
            for perm in required_perms:
                if perm not in permissoes:
                    raise ValidationError(f"Permission '{perm}' is required in permissoes")
                if not isinstance(permissoes[perm], bool):
                    raise ValidationError(f"Permission '{perm}' must be a boolean")
            
            self.service.create_user(
                user_id=user_id,
                nome=nome,
                permissoes=permissoes,
                ativo=ativo
            )
            
            return {
                'statusCode': 201,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'User created successfully',
                    'id': user_id
                })
            }
        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise
    
    def update_user(self, event: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Update an existing user
        
        Args:
            event: API Gateway event
            user_id: User email/identifier
            
        Returns:
            API Gateway response
        """
        try:
            body = json.loads(event.get('body', '{}'))
            
            nome = body.get('nome')
            permissoes = body.get('permissoes')
            ativo = body.get('ativo')
            
            if all(v is None for v in [nome, permissoes, ativo]):
                raise ValidationError("At least one field must be provided for update")
            
            # Validate permissoes if provided
            if permissoes is not None:
                if not isinstance(permissoes, dict):
                    raise ValidationError("Field 'permissoes' must be an object")
                
                required_perms = ['leitura', 'escrita', 'admin']
                for perm in required_perms:
                    if perm in permissoes and not isinstance(permissoes[perm], bool):
                        raise ValidationError(f"Permission '{perm}' must be a boolean")
            
            self.service.update_user(
                user_id=user_id,
                nome=nome,
                permissoes=permissoes,
                ativo=ativo
            )
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'User updated successfully',
                    'id': user_id
                })
            }
        except ValidationError:
            raise
        except ParameterNotFoundError as e:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            raise
    
    def delete_user(self, event: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Delete a user
        
        Args:
            event: API Gateway event
            user_id: User email/identifier
            
        Returns:
            API Gateway response
        """
        try:
            self.service.delete_user(user_id)
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'message': 'User deleted successfully',
                    'id': user_id
                })
            }
        except ParameterNotFoundError as e:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
            raise
