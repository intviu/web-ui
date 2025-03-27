"""
API routes for Gmail operations
"""
import logging
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Query, status
from ..dependencies import get_current_user_email
from ..database import get_user_credentials
from browser_use.tools.google_api import GmailTool

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/emails", tags=["email"])

# Model definitions
class EmailRequest(BaseModel):
    query: str = "is:inbox"
    maxResults: int = 10

class EmailResponse(BaseModel):
    emails: List[Dict[str, Any]]
    count: int
    success: bool
    error: Optional[str] = None

class EmailContentResponse(BaseModel):
    email: Optional[Dict[str, Any]] = None
    success: bool
    error: Optional[str] = None

class SendEmailRequest(BaseModel):
    to: str
    subject: str
    body: str
    cc: Optional[str] = None
    bcc: Optional[str] = None

class EmailResult(BaseModel):
    success: bool
    messageId: Optional[str] = None
    error: Optional[str] = None

class SendEmailResponse(BaseModel):
    result: EmailResult

# Helper function to get Gmail tool with user credentials
async def get_gmail_tool(user_email: str):
    credentials = await get_user_credentials(user_email)
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated with Google"
        )
    
    try:
        gmail_tool = GmailTool(credentials=credentials)
        return gmail_tool
    except Exception as e:
        logger.error(f"Failed to initialize Gmail tool: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize Gmail tool: {str(e)}"
        )

# API endpoints
@router.post("", response_model=EmailResponse)
async def list_emails(
    request: EmailRequest, 
    user_email: str = Depends(get_current_user_email)
):
    """
    Get a list of emails matching the provided query
    """
    try:
        gmail_tool = await get_gmail_tool(user_email)
        emails = await gmail_tool.list_emails(query=request.query, max_results=request.maxResults)
        
        return EmailResponse(
            emails=emails,
            count=len(emails),
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing emails: {str(e)}")
        return EmailResponse(
            emails=[],
            count=0,
            success=False,
            error=str(e)
        )

@router.get("/{email_id}", response_model=EmailContentResponse)
async def get_email_content(
    email_id: str,
    user_email: str = Depends(get_current_user_email)
):
    """
    Get the content of a specific email by ID
    """
    try:
        gmail_tool = await get_gmail_tool(user_email)
        email_content = await gmail_tool.get_email(email_id=email_id)
        
        return EmailContentResponse(
            email=email_content,
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting email content: {str(e)}")
        return EmailContentResponse(
            email=None,
            success=False,
            error=str(e)
        )

@router.post("/send", response_model=SendEmailResponse)
async def send_email(
    request: SendEmailRequest,
    user_email: str = Depends(get_current_user_email)
):
    """
    Send an email
    """
    try:
        gmail_tool = await get_gmail_tool(user_email)
        message_id = await gmail_tool.send_email(
            to=request.to,
            subject=request.subject,
            body=request.body,
            cc=request.cc,
            bcc=request.bcc
        )
        
        return SendEmailResponse(
            result=EmailResult(
                success=True,
                messageId=message_id
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return SendEmailResponse(
            result=EmailResult(
                success=False,
                error=str(e)
            )
        )

@router.post("/draft", response_model=SendEmailResponse)
async def create_draft(
    request: SendEmailRequest,
    user_email: str = Depends(get_current_user_email)
):
    """
    Create an email draft
    """
    try:
        gmail_tool = await get_gmail_tool(user_email)
        draft_id = await gmail_tool.create_draft(
            to=request.to,
            subject=request.subject,
            body=request.body,
            cc=request.cc,
            bcc=request.bcc
        )
        
        return SendEmailResponse(
            result=EmailResult(
                success=True,
                messageId=draft_id
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating draft: {str(e)}")
        return SendEmailResponse(
            result=EmailResult(
                success=False,
                error=str(e)
            )
        ) 