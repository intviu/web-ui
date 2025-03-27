"""
API routes for Google Calendar operations
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException, Query, status
from ..dependencies import get_current_user_email
from ..database import get_user_credentials
from browser_use.tools.google_api import GoogleCalendarTool

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/calendar", tags=["calendar"])

# Model definitions
class CalendarEvent(BaseModel):
    id: str
    summary: str
    start: Dict[str, Any]
    end: Dict[str, Any]
    location: Optional[str] = None
    description: Optional[str] = None
    attendees: Optional[List[Dict[str, Any]]] = None

class CalendarEventsResponse(BaseModel):
    events: List[CalendarEvent]
    count: int
    success: bool
    error: Optional[str] = None

class AvailabilityRequest(BaseModel):
    meetingDate: str = Field(..., description="Meeting date in ISO format")
    durationMinutes: int = Field(30, description="Duration of the meeting in minutes")

class AvailabilityResponse(BaseModel):
    available: bool
    conflicts: List[Dict[str, Any]] = []
    success: bool
    error: Optional[str] = None

class MeetingSuggestRequest(BaseModel):
    daysAhead: int = Field(5, description="Number of days to look ahead")
    durationMinutes: int = Field(30, description="Duration of the meeting in minutes")

class MeetingSuggestResponse(BaseModel):
    suggested_times: List[Dict[str, Any]]
    success: bool
    error: Optional[str] = None

# Helper function to get Calendar tool with user credentials
async def get_calendar_tool(user_email: str):
    credentials = await get_user_credentials(user_email)
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated with Google"
        )
    
    try:
        calendar_tool = GoogleCalendarTool(credentials=credentials)
        return calendar_tool
    except Exception as e:
        logger.error(f"Failed to initialize Calendar tool: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initialize Calendar tool: {str(e)}"
        )

# API endpoints
@router.get("/events", response_model=CalendarEventsResponse)
async def get_calendar_events(
    days: int = Query(7, description="Number of days to look ahead"),
    user_email: str = Depends(get_current_user_email)
):
    """
    Get calendar events for the next N days
    """
    try:
        calendar_tool = await get_calendar_tool(user_email)
        
        # Calculate time range
        start_time = datetime.now().isoformat() + 'Z'  # 'Z' indicates UTC time
        end_time = (datetime.now() + timedelta(days=days)).isoformat() + 'Z'
        
        events = await calendar_tool.list_events(
            start_time=start_time,
            end_time=end_time
        )
        
        return CalendarEventsResponse(
            events=events,
            count=len(events),
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting calendar events: {str(e)}")
        return CalendarEventsResponse(
            events=[],
            count=0,
            success=False,
            error=str(e)
        )

@router.post("/availability", response_model=AvailabilityResponse)
async def check_availability(
    request: AvailabilityRequest,
    user_email: str = Depends(get_current_user_email)
):
    """
    Check availability for a meeting time
    """
    try:
        calendar_tool = await get_calendar_tool(user_email)
        
        # Parse meeting date
        meeting_date = datetime.fromisoformat(request.meetingDate.replace('Z', '+00:00'))
        meeting_end = meeting_date + timedelta(minutes=request.durationMinutes)
        
        # Check availability
        available, conflicts = await calendar_tool.check_availability(
            start_time=meeting_date.isoformat(),
            end_time=meeting_end.isoformat()
        )
        
        return AvailabilityResponse(
            available=available,
            conflicts=conflicts,
            success=True
        )
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Invalid date format: {str(e)}")
        return AvailabilityResponse(
            available=False,
            success=False,
            error=f"Invalid date format: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error checking availability: {str(e)}")
        return AvailabilityResponse(
            available=False,
            success=False,
            error=str(e)
        )

@router.post("/suggest", response_model=MeetingSuggestResponse)
async def suggest_meeting_times(
    request: MeetingSuggestRequest,
    user_email: str = Depends(get_current_user_email)
):
    """
    Suggest available meeting times
    """
    try:
        calendar_tool = await get_calendar_tool(user_email)
        
        # Calculate time range
        start_time = datetime.now().isoformat() + 'Z'
        end_time = (datetime.now() + timedelta(days=request.daysAhead)).isoformat() + 'Z'
        
        # Get suggested times
        suggested_times = await calendar_tool.suggest_meeting_times(
            start_time=start_time,
            end_time=end_time,
            duration_minutes=request.durationMinutes
        )
        
        return MeetingSuggestResponse(
            suggested_times=suggested_times,
            success=True
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error suggesting meeting times: {str(e)}")
        return MeetingSuggestResponse(
            suggested_times=[],
            success=False,
            error=str(e)
        ) 