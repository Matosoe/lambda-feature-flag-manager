"""
User Repository for managing users in Parameter Store
"""
import logging
import boto3
import json
from typing import List, Dict, Any, Optional
from botocore.exceptions import ClientError
from src.exceptions import ParameterStoreError, ParameterNotFoundError

logger = logging.getLogger(__name__)


class UserRepository:
    """
    Repository for managing users stored in AWS Systems Manager Parameter Store
    All users are stored in a single parameter at /feature-flags/users
    """
    
    def __init__(self):
        self.ssm_client = boto3.client('ssm')
        self.users_path = '/feature-flags/users'
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Retrieve all users from Parameter Store
        
        Returns:
            List of user dictionaries
        """
        try:
            response = self.ssm_client.get_parameter(
                Name=self.users_path,
                WithDecryption=True
            )
            
            users_data = json.loads(response['Parameter']['Value'])
            return users_data.get('usuarios', [])
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == 'ParameterNotFound':
                # Initialize empty users structure
                logger.info("Users parameter not found, initializing...")
                self._initialize_users()
                return []
            logger.error(f"Error retrieving users: {str(e)}")
            raise ParameterStoreError(f"Failed to retrieve users: {str(e)}")
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific user by ID
        
        Args:
            user_id: User email/identifier
            
        Returns:
            User dictionary or None if not found
        """
        users = self.get_all_users()
        for user in users:
            if user.get('id') == user_id:
                return user
        return None
    
    def create_user(
        self,
        user_id: str,
        nome: str,
        permissoes: Dict[str, bool],
        ativo: bool = True
    ) -> None:
        """
        Create a new user
        
        Args:
            user_id: User email/identifier
            nome: User name
            permissoes: Permissions dict with leitura, escrita, admin
            ativo: Whether user is active
        """
        try:
            users = self.get_all_users()
            
            # Check if user already exists
            if any(u.get('id') == user_id for u in users):
                raise ParameterStoreError(f"User {user_id} already exists")
            
            # Add new user
            new_user = {
                'id': user_id,
                'nome': nome,
                'permissoes': permissoes,
                'ativo': ativo
            }
            users.append(new_user)
            
            # Save updated users
            self._save_users(users)
            logger.info(f"Successfully created user: {user_id}")
            
        except ClientError as e:
            logger.error(f"Error creating user: {str(e)}")
            raise ParameterStoreError(f"Failed to create user: {str(e)}")
    
    def update_user(
        self,
        user_id: str,
        nome: Optional[str] = None,
        permissoes: Optional[Dict[str, bool]] = None,
        ativo: Optional[bool] = None
    ) -> None:
        """
        Update an existing user
        
        Args:
            user_id: User email/identifier
            nome: New name (optional)
            permissoes: New permissions (optional)
            ativo: New active status (optional)
        """
        try:
            users = self.get_all_users()
            
            # Find user
            user_found = False
            for user in users:
                if user.get('id') == user_id:
                    user_found = True
                    if nome is not None:
                        user['nome'] = nome
                    if permissoes is not None:
                        user['permissoes'] = permissoes
                    if ativo is not None:
                        user['ativo'] = ativo
                    break
            
            if not user_found:
                raise ParameterNotFoundError(f"User {user_id} not found")
            
            # Save updated users
            self._save_users(users)
            logger.info(f"Successfully updated user: {user_id}")
            
        except ClientError as e:
            logger.error(f"Error updating user: {str(e)}")
            raise ParameterStoreError(f"Failed to update user: {str(e)}")
    
    def delete_user(self, user_id: str) -> None:
        """
        Delete a user
        
        Args:
            user_id: User email/identifier
        """
        try:
            users = self.get_all_users()
            
            # Filter out the user
            updated_users = [u for u in users if u.get('id') != user_id]
            
            if len(updated_users) == len(users):
                raise ParameterNotFoundError(f"User {user_id} not found")
            
            # Save updated users
            self._save_users(updated_users)
            logger.info(f"Successfully deleted user: {user_id}")
            
        except ClientError as e:
            logger.error(f"Error deleting user: {str(e)}")
            raise ParameterStoreError(f"Failed to delete user: {str(e)}")
    
    def _save_users(self, users: List[Dict[str, Any]]) -> None:
        """
        Save users list to Parameter Store
        
        Args:
            users: List of user dictionaries
        """
        users_data = {'usuarios': users}
        json_value = json.dumps(users_data, ensure_ascii=False)
        
        self.ssm_client.put_parameter(
            Name=self.users_path,
            Value=json_value,
            Description='Feature flags users with permissions',
            Type='String',
            Overwrite=True
        )
    
    def _initialize_users(self) -> None:
        """
        Initialize empty users structure in Parameter Store
        """
        self._save_users([])
