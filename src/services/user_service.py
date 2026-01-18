"""
User Service for business logic
"""
import logging
from typing import List, Dict, Any, Optional
from src.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    """
    Service for managing users
    """
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def list_users(self) -> List[Dict[str, Any]]:
        """
        List all users
        
        Returns:
            List of users
        """
        logger.info("Listing users")
        return self.repository.get_all_users()
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific user
        
        Args:
            user_id: User email/identifier
            
        Returns:
            User dictionary or None
        """
        logger.info(f"Getting user: {user_id}")
        return self.repository.get_user(user_id)
    
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
            permissoes: Permissions dict
            ativo: Whether user is active
        """
        logger.info(f"Creating user: {user_id}")
        self.repository.create_user(
            user_id=user_id,
            nome=nome,
            permissoes=permissoes,
            ativo=ativo
        )
    
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
        logger.info(f"Updating user: {user_id}")
        self.repository.update_user(
            user_id=user_id,
            nome=nome,
            permissoes=permissoes,
            ativo=ativo
        )
    
    def delete_user(self, user_id: str) -> None:
        """
        Delete a user
        
        Args:
            user_id: User email/identifier
        """
        logger.info(f"Deleting user: {user_id}")
        self.repository.delete_user(user_id)
