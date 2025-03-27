"""
Authentication routes for Google OAuth.
"""
import logging
import secrets
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from ..dependencies import get_current_user_email
from ..database import save_credentials, delete_user_credentials, get_user, save_user
from ..config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/auth", tags=["auth"])

# OAuth scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events.readonly'
]

# Model definitions
class GoogleAuthResponse(BaseModel):
    auth_url: str
    state: str

class GoogleAuthCallback(BaseModel):
    code: str
    state: str
    error: Optional[str] = None

class UserResponse(BaseModel):
    email: str
    authenticated: bool
    name: Optional[str] = None

# OAuth flow creation function
def create_oauth_flow(redirect_uri=None):
    """Create a new OAuth flow."""
    try:
        # Use client ID and secret from config
        client_config = {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [redirect_uri or GOOGLE_REDIRECT_URI]
            }
        }
        
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=redirect_uri or GOOGLE_REDIRECT_URI
        )
        return flow
    except Exception as e:
        logger.error(f"Failed to create OAuth flow: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create OAuth flow: {str(e)}"
        )

# API endpoints
@router.get("/google/login", response_model=GoogleAuthResponse)
async def login_google(request: Request):
    """
    Start Google OAuth login flow
    """
    try:
        # Set redirect URI
        redirect_uri = f"{request.base_url}api/auth/google/callback"
        flow = create_oauth_flow(redirect_uri)
        
        # Generate state token for CSRF protection
        state = secrets.token_urlsafe(32)
        
        # Generate authorization URL
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=state,
            prompt='consent'
        )
        
        # Store state in session for verification later
        request.session["oauth_state"] = state
        
        logger.info(f"Generated authorization URL with state: {state}")
        return GoogleAuthResponse(auth_url=auth_url, state=state)
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/google/callback", response_model=UserResponse)
async def google_callback(request: Request, code: Optional[str] = None, state: Optional[str] = None, error: Optional[str] = None):
    """
    Handle Google OAuth callback
    """
    # Check for errors
    if error:
        logger.error(f"OAuth error: {error}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth error: {error}"
        )
    
    # Validate required parameters
    if not code or not state:
        logger.error("Missing code or state parameter in callback")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing code or state parameter"
        )
    
    # Validate state to prevent CSRF
    session_state = request.session.get("oauth_state")
    if not session_state or session_state != state:
        logger.error(f"State mismatch: {state} vs {session_state}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state parameter"
        )
    
    try:
        # Set redirect URI
        redirect_uri = f"{request.base_url}api/auth/google/callback"
        flow = create_oauth_flow(redirect_uri)
        
        # Exchange code for tokens
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        # Get user info
        email = credentials.id_token.get('email')
        if not email:
            raise ValueError("Could not retrieve email from token")
        
        name = credentials.id_token.get('name', email.split('@')[0])
        
        # Save user and credentials
        await save_user(email, name)
        await save_credentials(
            email=email,
            credentials=credentials_to_dict(credentials),
            scopes=SCOPES
        )
        
        # Set session
        request.session["user_email"] = email
        
        logger.info(f"Successfully authenticated user: {email}")
        return UserResponse(email=email, authenticated=True, name=name)
    
    except Exception as e:
        logger.error(f"Callback error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/user", response_model=UserResponse)
async def get_current_user(request: Request):
    """
    Get current authenticated user
    """
    user_email = request.session.get("user_email")
    
    if not user_email:
        return UserResponse(email="", authenticated=False)
    
    try:
        user = await get_user(user_email)
        if user:
            return UserResponse(
                email=user["email"],
                authenticated=True,
                name=user["name"]
            )
        else:
            return UserResponse(email=user_email, authenticated=True)
    
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        return UserResponse(email="", authenticated=False)

@router.post("/logout")
async def logout(request: Request):
    """
    Logout user and clear session
    """
    try:
        user_email = request.session.get("user_email")
        
        if user_email:
            # Clear user session
            request.session.clear()
            logger.info(f"User logged out: {user_email}")
        
        return {"success": True}
    
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Helper functions
def credentials_to_dict(credentials):
    """Convert credentials to dictionary for storage."""
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
        'id_token': credentials._id_token,
    } 