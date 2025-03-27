"""
Shared dependencies for the API server.
"""
from fastapi import Depends, HTTPException, Request, status

# Dependency to get the current user's email from the session
def get_current_user_email(request: Request):
    """
    Get the current user's email from the session.
    
    Returns:
        str: The user's email
        
    Raises:
        HTTPException: If the user is not authenticated
    """
    if not hasattr(request, "session") or "user_email" not in request.session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return request.session.get("user_email") 