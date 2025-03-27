"""
Email view component for the browser use UI.
"""
import logging
import datetime
import json
from typing import Dict, List, Any, Optional, Callable
import asyncio

logger = logging.getLogger(__name__)

class EmailView:
    """Email view component for the browser use UI."""
    
    def __init__(self, email_agent, ui_callback: Optional[Callable] = None):
        """Initialize the EmailView.
        
        Args:
            email_agent: The email agent to use.
            ui_callback: Optional callback to update the UI.
        """
        self.email_agent = email_agent
        self.ui_callback = ui_callback
        self.emails = []
        self.events = []
        
    async def refresh_emails(self, query: str = "is:inbox", max_results: int = 20):
        """Refresh the emails list.
        
        Args:
            query: Gmail search query.
            max_results: Maximum number of results to return.
        """
        try:
            result = await self.email_agent.process({
                "action": "read_emails",
                "query": query,
                "max_results": max_results
            })
            
            self.emails = result.get("emails", [])
            logger.info(f"Refreshed {len(self.emails)} emails")
            
            if self.ui_callback:
                self.ui_callback({
                    "type": "emails_refreshed",
                    "emails": self.emails
                })
                
            return self.emails
        except Exception as e:
            logger.error(f"Error refreshing emails: {str(e)}")
            return []
            
    async def get_email(self, email_id: str):
        """Get the content of an email.
        
        Args:
            email_id: The ID of the email to get.
            
        Returns:
            Email object with content.
        """
        try:
            result = await self.email_agent.process({
                "action": "get_email",
                "email_id": email_id
            })
            
            email = result.get("email", {})
            
            if self.ui_callback:
                self.ui_callback({
                    "type": "email_loaded",
                    "email": email
                })
                
            return email
        except Exception as e:
            logger.error(f"Error getting email: {str(e)}")
            return {}
            
    async def compose_email(self, to: str, subject: str, body: str, cc: str = "", bcc: str = "",
                          is_draft: bool = False):
        """Compose and send/draft an email.
        
        Args:
            to: Recipient email address.
            subject: Email subject.
            body: Email body.
            cc: CC recipients.
            bcc: BCC recipients.
            is_draft: Whether to create a draft or send the email.
            
        Returns:
            Result of the operation.
        """
        try:
            action = "create_draft" if is_draft else "send_email"
            
            result = await self.email_agent.process({
                "action": action,
                "to": to,
                "subject": subject,
                "body": body,
                "cc": cc,
                "bcc": bcc
            })
            
            operation_result = result.get("result", {})
            
            if self.ui_callback:
                self.ui_callback({
                    "type": "email_composed",
                    "is_draft": is_draft,
                    "result": operation_result
                })
                
            return operation_result
        except Exception as e:
            logger.error(f"Error composing email: {str(e)}")
            return {"success": False, "error": str(e)}
            
    async def refresh_calendar(self, days: int = 7):
        """Refresh the calendar events.
        
        Args:
            days: Number of days to look ahead.
        """
        try:
            result = await self.email_agent.process({
                "action": "get_calendar_events",
                "days": days
            })
            
            self.events = result.get("events", [])
            logger.info(f"Refreshed {len(self.events)} calendar events")
            
            if self.ui_callback:
                self.ui_callback({
                    "type": "calendar_refreshed",
                    "events": self.events
                })
                
            return self.events
        except Exception as e:
            logger.error(f"Error refreshing calendar: {str(e)}")
            return []
            
    async def check_availability(self, meeting_date: str, duration_minutes: int = 30):
        """Check availability for a meeting.
        
        Args:
            meeting_date: Date string in ISO format.
            duration_minutes: Duration of meeting in minutes.
            
        Returns:
            Availability information.
        """
        try:
            result = await self.email_agent.process({
                "action": "check_availability",
                "meeting_date": meeting_date,
                "duration_minutes": duration_minutes
            })
            
            availability = result.get("availability", {})
            
            if self.ui_callback:
                self.ui_callback({
                    "type": "availability_checked",
                    "availability": availability
                })
                
            return availability
        except Exception as e:
            logger.error(f"Error checking availability: {str(e)}")
            return {"available": False, "error": str(e)}
            
    async def suggest_meeting_times(self, days_ahead: int = 5, duration_minutes: int = 30):
        """Suggest available meeting times.
        
        Args:
            days_ahead: Number of days to look ahead.
            duration_minutes: Duration of meeting in minutes.
            
        Returns:
            List of suggested meeting times.
        """
        try:
            result = await self.email_agent.process({
                "action": "suggest_meeting_times",
                "days_ahead": days_ahead,
                "duration_minutes": duration_minutes
            })
            
            suggested_times = result.get("suggested_times", [])
            
            if self.ui_callback:
                self.ui_callback({
                    "type": "meeting_times_suggested",
                    "suggested_times": suggested_times
                })
                
            return suggested_times
        except Exception as e:
            logger.error(f"Error suggesting meeting times: {str(e)}")
            return []
            
    def get_email_summary(self, count: int = 5):
        """Get a summary of recent emails.
        
        Args:
            count: Number of emails to include in summary.
            
        Returns:
            Summary string.
        """
        if not self.emails:
            return "No emails loaded. Please refresh emails first."
            
        summary = f"Recent {min(count, len(self.emails))} emails:\n"
        
        for i, email in enumerate(self.emails[:count]):
            sender = email.get("sender", "Unknown")
            subject = email.get("subject", "No subject")
            date = email.get("date", "Unknown date")
            
            summary += f"{i+1}. From: {sender} - Subject: {subject} - Date: {date}\n"
            
        return summary
        
    def get_calendar_summary(self, count: int = 5):
        """Get a summary of upcoming calendar events.
        
        Args:
            count: Number of events to include in summary.
            
        Returns:
            Summary string.
        """
        if not self.events:
            return "No calendar events loaded. Please refresh calendar first."
            
        summary = f"Upcoming {min(count, len(self.events))} events:\n"
        
        for i, event in enumerate(self.events[:count]):
            title = event.get("summary", "Untitled")
            start = event.get("start", {}).get("dateTime", "Unknown time")
            location = event.get("location", "No location")
            
            if isinstance(start, str):
                try:
                    start_dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
                    start = start_dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass
                
            summary += f"{i+1}. {title} - {start} - {location}\n"
            
        return summary 