"""
Authorization middleware for validating user permissions
"""
import logging
from typing import Dict, Any, Optional
from src.repositories.user_repository import UserRepository
from src.exceptions import ValidationError

logger = logging.getLogger(__name__)


class AuthorizationMiddleware:
    """
    Middleware for handling user authentication and authorization
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def validate_permission(
        self,
        user_id: str,
        required_permission: str
    ) -> None:
        """
        Validate if user has required permission
        
        Args:
            user_id: User email/identifier
            required_permission: One of 'leitura', 'escrita', 'admin'
            
        Raises:
            ValidationError: If user doesn't have permission or is inactive
        """
        if not user_id:
            raise ValidationError("User ID is required in header 'X-User-Id'")
        
        user = self.user_repository.get_user(user_id)
        
        if not user:
            raise ValidationError(f"User {user_id} not found")
        
        if not user.get('ativo', False):
            raise ValidationError(f"User {user_id} is inactive")
        
        permissoes = user.get('permissoes', {})
        
        # Admin has all permissions
        if permissoes.get('admin', False):
            return
        
        # Check specific permission
        if not permissoes.get(required_permission, False):
            raise ValidationError(
                f"User {user_id} does not have '{required_permission}' permission"
            )
    
    def get_user_from_event(self, event: Dict[str, Any]) -> Optional[str]:
        """
        Extract user ID from API Gateway event headers
        
        Args:
            event: API Gateway event
            
        Returns:
            User ID or None
        """
        headers = event.get('headers', {})
        
        # Try different header formats (case-insensitive)
        for key in headers:
            if key.lower() == 'x-user-id':
                return headers[key]
        
        return None
    
    def is_admin(self, user_id: str) -> bool:
        """
        Check if user is admin
        
        Args:
            user_id: User email/identifier
            
        Returns:
            True if user is admin, False otherwise
        """
        try:
            user = self.user_repository.get_user(user_id)
            if not user or not user.get('ativo', False):
                return False
            return user.get('permissoes', {}).get('admin', False)
        except Exception as e:
            logger.error(f"Error checking admin status: {str(e)}")
            return False
