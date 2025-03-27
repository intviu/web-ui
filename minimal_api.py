from fastapi import FastAPI, Request, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import logging
import secrets
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Virtual Business Manager API")

# Configuration
CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8001",
]

SESSION_SECRET = os.getenv("SESSION_SECRET", secrets.token_urlsafe(32))

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add session middleware
app.add_middleware(
    SessionMiddleware, 
    secret_key=SESSION_SECRET,
    session_cookie="vbm_session",
    max_age=30 * 24 * 60 * 60,  # 30 days in seconds
)

# Models for API requests and responses
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

class CalendarEventResponse(BaseModel):
    events: List[Dict[str, Any]]
    success: bool
    error: Optional[str] = None

class AvailabilityRequest(BaseModel):
    meetingDate: str
    durationMinutes: int = 30

class AvailabilityResponse(BaseModel):
    is_available: bool
    conflicts: List[Dict[str, Any]] = []
    success: bool
    error: Optional[str] = None

class SuggestTimesRequest(BaseModel):
    daysAhead: int = 5
    durationMinutes: int = 30

class SuggestTimesResponse(BaseModel):
    suggested_times: List[Dict[str, Any]] = []
    success: bool
    error: Optional[str] = None

# Root endpoint
@app.get("/")
async def root():
    logger.info("Root endpoint requested")
    return {"message": "Welcome to the Virtual Business Manager API"}

# Health endpoints
@app.get("/health")
async def health():
    logger.info("Health endpoint requested")
    return {"status": "healthy"}

@app.get("/api/health")
async def api_health():
    logger.info("API health endpoint requested")
    return {"status": "healthy", "path": "api/health"}

@app.get("/api/healthcheck")
async def healthcheck():
    logger.info("API healthcheck endpoint requested")
    return {"status": "healthy", "type": "healthcheck"}

# User session management
def get_current_user_email(request: Request):
    """Get the current user's email from the session."""
    if not hasattr(request, "session") or "user_email" not in request.session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return request.session.get("user_email")

# User endpoint
@app.get("/api/auth/user")
async def get_current_user(request: Request):
    """Get current authenticated user"""
    user_email = request.session.get("user_email")
    
    if not user_email:
        return {"email": "", "authenticated": False}
    
    return {"email": user_email, "authenticated": True, "name": user_email.split('@')[0]}

# Google OAuth endpoint
@app.get("/api/auth/google/login")
async def login_google(request: Request):
    """Start Google OAuth login flow"""
    logger.info("Google login request")
    
    # Generate mock auth URL
    state = secrets.token_urlsafe(16)
    request.session["oauth_state"] = state
    
    # In a real app, this would redirect to Google
    # Use an absolute URL
    auth_url = f"http://localhost:3000/auth/google/callback?state={state}&code=mock_auth_code"
    
    return {"auth_url": auth_url, "state": state}

# Login/logout endpoints
@app.post("/api/auth/login")
async def login(request: Request):
    """Simple mock login"""
    request.session["user_email"] = "user@example.com"
    logger.info("User logged in: user@example.com")
    return {"success": True}

@app.post("/api/auth/logout")
async def logout(request: Request):
    """Simple mock logout"""
    request.session.clear()
    logger.info("User logged out")
    return {"success": True}

# Email endpoints
@app.post("/api/emails", response_model=EmailResponse)
async def list_emails(
    request: EmailRequest, 
    request_obj: Request
):
    """Get a list of emails matching the provided query"""
    logger.info(f"List emails request: {request.query}")
    
    # Generate mock emails
    mock_emails = [
        {
            "id": f"email_{i}",
            "snippet": f"This is email snippet {i}",
            "subject": f"Test Email {i}",
            "from": "sender@example.com",
            "to": request_obj.session.get("user_email", "user@example.com"),
            "date": (datetime.now() - timedelta(hours=i)).isoformat(),
            "hasAttachment": i % 3 == 0,
            "isUnread": i % 2 == 0
        }
        for i in range(1, request.maxResults + 1)
    ]
    
    return EmailResponse(
        emails=mock_emails,
        count=len(mock_emails),
        success=True
    )

@app.get("/api/emails/{email_id}", response_model=EmailContentResponse)
async def get_email_content(
    email_id: str,
    request: Request
):
    """Get the content of a specific email by ID"""
    logger.info(f"Get email content: {email_id}")
    
    # Generate mock email content
    id_num = email_id.split('_')[-1] if '_' in email_id else '0'
    
    try:
        num = int(id_num)
        mock_email = {
            "id": email_id,
            "snippet": f"This is email snippet {num}",
            "subject": f"Test Email {num}",
            "from": "sender@example.com",
            "to": request.session.get("user_email", "user@example.com"),
            "date": (datetime.now() - timedelta(hours=num)).isoformat(),
            "body": f"This is the full body content of email {num}.\n\nLorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum euismod porttitor diam vitae rhoncus.\n\nRegards,\nSender",
            "hasAttachment": num % 3 == 0,
            "isUnread": num % 2 == 0,
            "attachments": [
                {"name": f"attachment_{num}_1.pdf", "size": 1024 * (num + 1)}
            ] if num % 3 == 0 else []
        }
        
        return EmailContentResponse(
            email=mock_email,
            success=True
        )
    except ValueError:
        return EmailContentResponse(
            email=None,
            success=False,
            error=f"Invalid email ID: {email_id}"
        )

@app.post("/api/emails/send", response_model=SendEmailResponse)
async def send_email(
    request: SendEmailRequest
):
    """Send an email"""
    logger.info(f"Send email: To {request.to}, Subject: {request.subject}")
    
    # Mock sending an email
    message_id = f"msg_{secrets.token_hex(8)}"
    
    return SendEmailResponse(
        result=EmailResult(
            success=True,
            messageId=message_id
        )
    )

@app.post("/api/emails/draft", response_model=SendEmailResponse)
async def create_draft(
    request: SendEmailRequest
):
    """Create an email draft"""
    logger.info(f"Create draft: To {request.to}, Subject: {request.subject}")
    
    # Mock creating a draft
    message_id = f"draft_{secrets.token_hex(8)}"
    
    return SendEmailResponse(
        result=EmailResult(
            success=True,
            messageId=message_id
        )
    )

# Calendar endpoints
@app.get("/api/calendar/events", response_model=CalendarEventResponse)
async def list_events(
    days: int = Query(7, description="Number of days to look ahead")
):
    """Get calendar events for the next N days"""
    logger.info(f"List calendar events for next {days} days")
    
    # Generate mock calendar events
    now = datetime.now()
    mock_events = []
    
    for i in range(days):
        day_date = now + timedelta(days=i)
        
        # Create 0-3 events per day
        num_events = secrets.randbelow(4)
        for j in range(num_events):
            start_hour = 9 + secrets.randbelow(8)  # Events between 9 AM and 5 PM
            duration = 30 * (1 + secrets.randbelow(4))  # 30, 60, 90, or 120 minutes
            
            start_time = day_date.replace(hour=start_hour, minute=0, second=0, microsecond=0)
            end_time = start_time + timedelta(minutes=duration)
            
            mock_events.append({
                "id": f"event_{i}_{j}",
                "summary": f"Meeting {i}.{j}",
                "description": f"This is a mock calendar event for testing purposes",
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "location": "Virtual",
                "attendees": [
                    {"email": "attendee1@example.com", "name": "Attendee 1", "responseStatus": "accepted"},
                    {"email": "attendee2@example.com", "name": "Attendee 2", "responseStatus": "tentative"}
                ]
            })
    
    return CalendarEventResponse(
        events=mock_events,
        success=True
    )

@app.post("/api/calendar/availability", response_model=AvailabilityResponse)
async def check_availability(
    request: AvailabilityRequest
):
    """Check availability for a specific time slot"""
    logger.info(f"Check availability for {request.meetingDate}, duration: {request.durationMinutes} minutes")
    
    # Mock availability check - 80% chance of being available
    is_available = secrets.randbelow(10) < 8
    conflicts = []
    
    if not is_available:
        # Create a mock conflict
        try:
            meeting_date = datetime.fromisoformat(request.meetingDate.replace('Z', '+00:00'))
            conflict_start = meeting_date - timedelta(minutes=15)
            conflict_end = meeting_date + timedelta(minutes=45)
            
            conflicts.append({
                "id": "conflict_event",
                "summary": "Existing Meeting",
                "start": conflict_start.isoformat(),
                "end": conflict_end.isoformat()
            })
        except ValueError:
            pass
    
    return AvailabilityResponse(
        is_available=is_available,
        conflicts=conflicts,
        success=True
    )

@app.post("/api/calendar/suggest", response_model=SuggestTimesResponse)
async def suggest_meeting_times(
    request: SuggestTimesRequest
):
    """Suggest available meeting times"""
    logger.info(f"Suggest meeting times for next {request.daysAhead} days, duration: {request.durationMinutes} minutes")
    
    # Generate mock time suggestions
    now = datetime.now()
    suggested_times = []
    
    for i in range(1, request.daysAhead + 1):
        day_date = now + timedelta(days=i)
        
        # Suggest 2 times per day
        for hour in [10, 14]:  # 10 AM and 2 PM
            start_time = day_date.replace(hour=hour, minute=0, second=0, microsecond=0)
            end_time = start_time + timedelta(minutes=request.durationMinutes)
            
            suggested_times.append({
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "conflicts": []  # No conflicts for suggested times
            })
    
    return SuggestTimesResponse(
        suggested_times=suggested_times,
        success=True
    )

# Google auth callback
@app.get("/api/auth/google/callback")
async def google_callback(
    request: Request,
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None
):
    """Handle Google OAuth callback"""
    logger.info(f"Google auth callback: code={code}, state={state}, error={error}")
    
    if error:
        return {
            "success": False,
            "error": f"Authentication error: {error}"
        }
    
    if not code:
        return {
            "success": False,
            "error": "Missing authorization code"
        }
    
    # In a real app, we would validate the state and exchange the code for tokens
    
    # Set user in session
    user_email = "user@example.com"
    request.session["user_email"] = user_email
    
    return {
        "success": True,
        "email": user_email,
        "authenticated": True,
        "name": user_email.split('@')[0]
    }

# Start server
if __name__ == "__main__":
    logger.info("Starting minimal API server on port 8001")
    uvicorn.run(app, host="0.0.0.0", port=8001) 