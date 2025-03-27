"""
EmailAgent for handling email operations with Gmail and Google Calendar.
"""
import logging
import json
import datetime
from typing import Dict, List, Any, Optional
from ..tools.google_api import GmailTool, GoogleCalendarTool
from .agent import Agent

logger = logging.getLogger(__name__)

class EmailAgent(Agent):
    """Agent for handling email operations."""
    
    def __init__(self, task: str, llm: Any, **kwargs):
        """Initialize the EmailAgent.
        
        Args:
            task: The task to perform.
            llm: The language model to use.
            **kwargs: Additional arguments to pass to the parent class.
                credentials_path: Path to Google API credentials file.
                token_path: Path to token file.
                user_email: Email address of the user (for database credentials).
        """
        super().__init__(task, llm, **kwargs)
        
        # Initialize the Gmail and Calendar tools
        self.gmail_tool = GmailTool(
            token_path=kwargs.get("token_path"),
            credentials_path=kwargs.get("credentials_path"),
            user_email=kwargs.get("user_email")
        )
        self.calendar_tool = GoogleCalendarTool(
            token_path=kwargs.get("token_path"),
            credentials_path=kwargs.get("credentials_path"),
            user_email=kwargs.get("user_email")
        )
        
    async def read_emails(self, query: str = "", max_results: int = 10) -> List[Dict[str, Any]]:
        """Read emails matching the query.
        
        Args:
            query: Gmail search query (e.g., "is:unread").
            max_results: Maximum number of results to return.
            
        Returns:
            List of email objects.
        """
        try:
            logger.info(f"Reading emails with query: {query}")
            emails = await self.gmail_tool.list_emails(query, max_results)
            return emails
        except Exception as e:
            logger.error(f"Error reading emails: {str(e)}")
            return []
            
    async def get_email_content(self, email_id: str) -> Dict[str, Any]:
        """Get the content of an email.
        
        Args:
            email_id: The ID of the email to get.
            
        Returns:
            Email object with content.
        """
        try:
            logger.info(f"Getting email content for ID: {email_id}")
            email = await self.gmail_tool.get_email(email_id)
            return email
        except Exception as e:
            logger.error(f"Error getting email content: {str(e)}")
            return {}
            
    async def send_email(self, to: str, subject: str, body: str, cc: str = "", bcc: str = "") -> Dict[str, Any]:
        """Send an email.
        
        Args:
            to: Recipient email address.
            subject: Email subject.
            body: Email body.
            cc: CC recipients.
            bcc: BCC recipients.
            
        Returns:
            Result of the operation.
        """
        try:
            logger.info(f"Sending email to: {to}")
            result = await self.gmail_tool.send_email(to, subject, body, cc, bcc)
            return result
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return {"success": False, "error": str(e)}
            
    async def create_draft(self, to: str, subject: str, body: str, cc: str = "", bcc: str = "") -> Dict[str, Any]:
        """Create a draft email.
        
        Args:
            to: Recipient email address.
            subject: Email subject.
            body: Email body.
            cc: CC recipients.
            bcc: BCC recipients.
            
        Returns:
            Result of the operation.
        """
        try:
            logger.info(f"Creating draft email to: {to}")
            result = await self.gmail_tool.create_draft(to, subject, body, cc, bcc)
            return result
        except Exception as e:
            logger.error(f"Error creating draft: {str(e)}")
            return {"success": False, "error": str(e)}
            
    async def get_calendar_events(self, 
                                days: int = 7, 
                                calendar_id: str = "primary") -> List[Dict[str, Any]]:
        """Get calendar events for the next N days.
        
        Args:
            days: Number of days to look ahead.
            calendar_id: Calendar ID (use "primary" for primary calendar).
            
        Returns:
            List of event objects.
        """
        try:
            logger.info(f"Getting calendar events for the next {days} days")
            time_min = datetime.datetime.utcnow()
            time_max = time_min + datetime.timedelta(days=days)
            
            events = await self.calendar_tool.get_events(
                calendar_id=calendar_id,
                time_min=time_min,
                time_max=time_max
            )
            return events
        except Exception as e:
            logger.error(f"Error getting calendar events: {str(e)}")
            return []
            
    async def check_availability(self, 
                              meeting_date: str,
                              duration_minutes: int = 30) -> Dict[str, Any]:
        """Check availability for a meeting.
        
        Args:
            meeting_date: Date string in ISO format (e.g., "2023-07-15T14:00:00").
            duration_minutes: Duration of meeting in minutes.
            
        Returns:
            Availability information.
        """
        try:
            logger.info(f"Checking availability for {meeting_date}")
            time_min = datetime.datetime.fromisoformat(meeting_date.replace("Z", "+00:00"))
            time_max = time_min + datetime.timedelta(minutes=duration_minutes)
            
            availability = await self.calendar_tool.check_availability(
                time_min=time_min,
                time_max=time_max
            )
            return availability
        except Exception as e:
            logger.error(f"Error checking availability: {str(e)}")
            return {"available": False, "error": str(e)}
            
    async def suggest_meeting_times(self, 
                                 days_ahead: int = 5,
                                 duration_minutes: int = 30) -> List[Dict[str, Any]]:
        """Suggest available meeting times.
        
        Args:
            days_ahead: Number of days to look ahead.
            duration_minutes: Duration of meeting in minutes.
            
        Returns:
            List of suggested meeting times.
        """
        try:
            logger.info(f"Suggesting meeting times for the next {days_ahead} days")
            time_min = datetime.datetime.utcnow()
            time_max = time_min + datetime.timedelta(days=days_ahead)
            
            suggested_times = await self.calendar_tool.suggest_meeting_times(
                duration_minutes=duration_minutes,
                time_min=time_min,
                time_max=time_max
            )
            return suggested_times
        except Exception as e:
            logger.error(f"Error suggesting meeting times: {str(e)}")
            return [{"error": str(e)}]
            
    async def _process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data.
        
        Args:
            input_data: Input data.
            
        Returns:
            Processing result.
        """
        logger.info(f"Processing input: {json.dumps(input_data)}")
        
        # Process input data based on action
        action = input_data.get("action", "")
        
        if action == "read_emails":
            emails = await self.read_emails(
                query=input_data.get("query", ""),
                max_results=input_data.get("max_results", 10)
            )
            return {"emails": emails}
            
        elif action == "get_email":
            email = await self.get_email_content(
                email_id=input_data.get("email_id", "")
            )
            return {"email": email}
            
        elif action == "send_email":
            result = await self.send_email(
                to=input_data.get("to", ""),
                subject=input_data.get("subject", ""),
                body=input_data.get("body", ""),
                cc=input_data.get("cc", ""),
                bcc=input_data.get("bcc", "")
            )
            return {"result": result}
            
        elif action == "create_draft":
            result = await self.create_draft(
                to=input_data.get("to", ""),
                subject=input_data.get("subject", ""),
                body=input_data.get("body", ""),
                cc=input_data.get("cc", ""),
                bcc=input_data.get("bcc", "")
            )
            return {"result": result}
            
        elif action == "get_calendar_events":
            events = await self.get_calendar_events(
                days=input_data.get("days", 7),
                calendar_id=input_data.get("calendar_id", "primary")
            )
            return {"events": events}
            
        elif action == "check_availability":
            availability = await self.check_availability(
                meeting_date=input_data.get("meeting_date", ""),
                duration_minutes=input_data.get("duration_minutes", 30)
            )
            return {"availability": availability}
            
        elif action == "suggest_meeting_times":
            suggested_times = await self.suggest_meeting_times(
                days_ahead=input_data.get("days_ahead", 5),
                duration_minutes=input_data.get("duration_minutes", 30)
            )
            return {"suggested_times": suggested_times}
            
        else:
            logger.warning(f"Unknown action: {action}")
            return {"error": f"Unknown action: {action}"}
            
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data.
        
        Args:
            input_data: Input data.
            
        Returns:
            Processing result.
        """
        # If input_data is a string, convert it to a dict
        if isinstance(input_data, str):
            input_data = {"message": input_data}
            
        # Extract action from message if not specified
        if "action" not in input_data and "message" in input_data:
            message = input_data["message"].lower()
            
            if "read" in message and "email" in message:
                input_data["action"] = "read_emails"
                
            elif "get" in message and "email" in message:
                input_data["action"] = "get_email"
                
            elif "send" in message and "email" in message:
                input_data["action"] = "send_email"
                
            elif "draft" in message:
                input_data["action"] = "create_draft"
                
            elif "calendar" in message:
                input_data["action"] = "get_calendar_events"
                
            elif "availability" in message or "free" in message:
                input_data["action"] = "check_availability"
                
            elif "suggest" in message and "time" in message:
                input_data["action"] = "suggest_meeting_times"
        
        # Process the input
        try:
            result = await self._process_input(input_data)
            
            # Add metadata
            result["metadata"] = {
                "agent": self.__class__.__name__,
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            
            return result
        except Exception as e:
            logger.error(f"Error processing input: {str(e)}")
            return {
                "error": str(e),
                "metadata": {
                    "agent": self.__class__.__name__,
                    "timestamp": datetime.datetime.utcnow().isoformat()
                }
            } 