"""
Google OAuth authentication utilities.
"""
import logging
from typing import Dict, Any

# Setup logging
logger = logging.getLogger(__name__)

async def load_credentials_from_db(email: str) -> Dict[str, Any]:
    """
    Load credentials from the database for a specific user.
    
    Args:
        email: The email of the user
        
    Returns:
        The credentials dictionary
    """
    # Import here to avoid circular imports
    from api.database import get_user_credentials
    
    credentials = await get_user_credentials(email)
    if not credentials:
        raise ValueError(f"No credentials found for user {email}")
    
    return credentials 