"""
Google API tools for interacting with Gmail and Google Calendar.
"""
import base64
import logging
import email.mime.text
import email.mime.multipart
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import dependencies avoiding circular imports
# Define import function to be used when needed
async def get_credentials_from_db(email: str) -> Dict[str, Any]:
    from api.database import get_user_credentials
    
    credentials = await get_user_credentials(email)
    if not credentials:
        raise ValueError(f"No credentials found for user {email}")
    
    return credentials

# Setup logging
logger = logging.getLogger(__name__)

class GoogleAPIMixin:
    """Base class for Google API tools."""
    
    def __init__(self, credentials: Dict[str, Any] = None, user_email: str = None):
        """
        Initialize the Google API tool.
        
        Args:
            credentials: Google API credentials dictionary
            user_email: User's email address to load credentials from database
        """
        if not credentials and not user_email:
            raise ValueError("Either credentials or user_email must be provided")
        
        self.credentials = credentials
        self.user_email = user_email
        self._service = None
    
    async def _get_service(self, api_name: str, api_version: str):
        """
        Get or create an API service.
        
        Args:
            api_name: Name of the API
            api_version: Version of the API
            
        Returns:
            The API service
        """
        if self._service is None:
            if self.credentials is None and self.user_email:
                self.credentials = await get_credentials_from_db(self.user_email)
            
            creds = Credentials(
                token=self.credentials.get('token'),
                refresh_token=self.credentials.get('refresh_token'),
                token_uri=self.credentials.get('token_uri'),
                client_id=self.credentials.get('client_id'),
                client_secret=self.credentials.get('client_secret'),
                scopes=self.credentials.get('scopes')
            )
            
            self._service = build(api_name, api_version, credentials=creds)
        
        return self._service


class GmailTool(GoogleAPIMixin):
    """Tool for interacting with Gmail API."""
    
    async def list_emails(self, query: str = 'is:inbox', max_results: int = 10) -> List[Dict[str, Any]]:
        """
        List emails matching the query.
        
        Args:
            query: Gmail search query
            max_results: Maximum number of results to return
            
        Returns:
            List of email metadata
        """
        try:
            service = await self._get_service('gmail', 'v1')
            result = service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = result.get('messages', [])
            emails = []
            
            for message in messages:
                msg = service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='metadata',
                    metadataHeaders=['From', 'To', 'Subject', 'Date']
                ).execute()
                
                headers = msg['payload']['headers']
                email_data = {
                    'id': msg['id'],
                    'threadId': msg['threadId'],
                    'snippet': msg.get('snippet', ''),
                    'labelIds': msg.get('labelIds', [])
                }
                
                for header in headers:
                    if header['name'] == 'From':
                        email_data['sender'] = header['value']
                    elif header['name'] == 'To':
                        email_data['to'] = header['value']
                    elif header['name'] == 'Subject':
                        email_data['subject'] = header['value']
                    elif header['name'] == 'Date':
                        email_data['date'] = header['value']
                
                emails.append(email_data)
            
            return emails
        
        except HttpError as error:
            logger.error(f"Error listing emails: {error}")
            raise
    
    async def get_email(self, email_id: str) -> Dict[str, Any]:
        """
        Get an email by ID.
        
        Args:
            email_id: ID of the email to retrieve
            
        Returns:
            Email data including content
        """
        try:
            service = await self._get_service('gmail', 'v1')
            msg = service.users().messages().get(
                userId='me',
                id=email_id,
                format='full'
            ).execute()
            
            headers = msg['payload']['headers']
            email_data = {
                'id': msg['id'],
                'threadId': msg['threadId'],
                'snippet': msg.get('snippet', ''),
                'labelIds': msg.get('labelIds', [])
            }
            
            for header in headers:
                if header['name'] == 'From':
                    email_data['sender'] = header['value']
                elif header['name'] == 'To':
                    email_data['to'] = header['value']
                elif header['name'] == 'Subject':
                    email_data['subject'] = header['value']
                elif header['name'] == 'Date':
                    email_data['date'] = header['value']
                elif header['name'] == 'Cc':
                    email_data['cc'] = header['value']
                elif header['name'] == 'Bcc':
                    email_data['bcc'] = header['value']
            
            # Get the email body
            body = ''
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = base64.urlsafe_b64decode(
                            part['body']['data'].encode('ASCII')
                        ).decode('utf-8')
                        break
            elif 'body' in msg['payload'] and 'data' in msg['payload']['body']:
                body = base64.urlsafe_b64decode(
                    msg['payload']['body']['data'].encode('ASCII')
                ).decode('utf-8')
            
            email_data['body'] = body
            
            return email_data
        
        except HttpError as error:
            logger.error(f"Error getting email: {error}")
            raise
    
    async def send_email(
        self, 
        to: str, 
        subject: str, 
        body: str, 
        cc: Optional[str] = None, 
        bcc: Optional[str] = None
    ) -> str:
        """
        Send an email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            cc: Carbon copy recipients
            bcc: Blind carbon copy recipients
            
        Returns:
            ID of the sent message
        """
        try:
            service = await self._get_service('gmail', 'v1')
            
            message = email.mime.multipart.MIMEMultipart()
            message['to'] = to
            message['subject'] = subject
            
            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc
            
            msg = email.mime.text.MIMEText(body)
            message.attach(msg)
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            result = service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            return result['id']
        
        except HttpError as error:
            logger.error(f"Error sending email: {error}")
            raise
    
    async def create_draft(
        self, 
        to: str, 
        subject: str, 
        body: str, 
        cc: Optional[str] = None, 
        bcc: Optional[str] = None
    ) -> str:
        """
        Create an email draft.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            cc: Carbon copy recipients
            bcc: Blind carbon copy recipients
            
        Returns:
            ID of the created draft
        """
        try:
            service = await self._get_service('gmail', 'v1')
            
            message = email.mime.multipart.MIMEMultipart()
            message['to'] = to
            message['subject'] = subject
            
            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc
            
            msg = email.mime.text.MIMEText(body)
            message.attach(msg)
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            draft = service.users().drafts().create(
                userId='me',
                body={
                    'message': {
                        'raw': raw_message
                    }
                }
            ).execute()
            
            return draft['id']
        
        except HttpError as error:
            logger.error(f"Error creating draft: {error}")
            raise


class GoogleCalendarTool(GoogleAPIMixin):
    """Tool for interacting with Google Calendar API."""
    
    async def list_events(
        self, 
        start_time: str, 
        end_time: str, 
        calendar_id: str = 'primary'
    ) -> List[Dict[str, Any]]:
        """
        List calendar events.
        
        Args:
            start_time: Start time in ISO format
            end_time: End time in ISO format
            calendar_id: Calendar ID, default is primary calendar
            
        Returns:
            List of calendar events
        """
        try:
            service = await self._get_service('calendar', 'v3')
            
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=start_time,
                timeMax=end_time,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            return events
        
        except HttpError as error:
            logger.error(f"Error listing calendar events: {error}")
            raise
    
    async def check_availability(
        self, 
        start_time: str, 
        end_time: str, 
        calendar_id: str = 'primary'
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Check if a time slot is available.
        
        Args:
            start_time: Start time in ISO format
            end_time: End time in ISO format
            calendar_id: Calendar ID, default is primary calendar
            
        Returns:
            Tuple containing (is_available, conflicting_events)
        """
        try:
            service = await self._get_service('calendar', 'v3')
            
            # Convert strings to datetime for comparison
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            
            # Get events in the time range
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=start_time,
                timeMax=end_time,
                singleEvents=True
            ).execute()
            
            events = events_result.get('items', [])
            
            # Filter events that actually conflict
            conflicts = []
            for event in events:
                event_start = event.get('start', {})
                event_end = event.get('end', {})
                
                # Skip events without start or end times
                if not event_start or not event_end:
                    continue
                
                # Get event start and end times
                event_start_time = event_start.get('dateTime', event_start.get('date'))
                event_end_time = event_end.get('dateTime', event_end.get('date'))
                
                if not event_start_time or not event_end_time:
                    continue
                    
                # Convert to datetime
                event_start_dt = datetime.fromisoformat(event_start_time.replace('Z', '+00:00'))
                event_end_dt = datetime.fromisoformat(event_end_time.replace('Z', '+00:00'))
                
                # Check for overlap
                if (start_dt < event_end_dt and end_dt > event_start_dt):
                    conflicts.append(event)
            
            is_available = len(conflicts) == 0
            
            return (is_available, conflicts)
        
        except HttpError as error:
            logger.error(f"Error checking availability: {error}")
            raise
    
    async def suggest_meeting_times(
        self, 
        start_time: str,
        end_time: str,
        duration_minutes: int = 30,
        calendar_id: str = 'primary',
        working_hours: Tuple[int, int] = (9, 17),  # 9 AM to 5 PM
        days_to_check: int = None
    ) -> List[Dict[str, str]]:
        """
        Suggest available meeting times.
        
        Args:
            start_time: Start time in ISO format
            end_time: End time in ISO format
            duration_minutes: Duration of the meeting in minutes
            calendar_id: Calendar ID, default is primary calendar
            working_hours: Tuple of start and end hours (24 hour format)
            days_to_check: Number of days to check, if None will use the range from start_time to end_time
            
        Returns:
            List of available time slots with start and end times
        """
        try:
            service = await self._get_service('calendar', 'v3')
            
            # Convert start and end times to datetime
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            
            # If days_to_check is provided, use it instead of the end_time
            if days_to_check is not None:
                end_dt = start_dt + timedelta(days=days_to_check)
                end_time = end_dt.isoformat() + 'Z'
            
            # Get all events in the range
            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=start_time,
                timeMax=end_time,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            all_events = events_result.get('items', [])
            
            # Extract busy times
            busy_slots = []
            for event in all_events:
                event_start = event.get('start', {})
                event_end = event.get('end', {})
                
                # Skip events without start or end times
                if not event_start or not event_end:
                    continue
                
                # Get event start and end times
                event_start_time = event_start.get('dateTime', event_start.get('date'))
                event_end_time = event_end.get('dateTime', event_end.get('date'))
                
                if not event_start_time or not event_end_time:
                    continue
                
                # Convert to datetime
                event_start_dt = datetime.fromisoformat(event_start_time.replace('Z', '+00:00'))
                event_end_dt = datetime.fromisoformat(event_end_time.replace('Z', '+00:00'))
                
                busy_slots.append((event_start_dt, event_end_dt))
            
            # Generate potential meeting slots
            available_slots = []
            current_day = start_dt.replace(hour=working_hours[0], minute=0, second=0, microsecond=0)
            meeting_duration = timedelta(minutes=duration_minutes)
            
            # Skip to the next day if we're starting after working hours
            if current_day.hour >= working_hours[1]:
                current_day = (current_day + timedelta(days=1)).replace(
                    hour=working_hours[0], minute=0, second=0, microsecond=0
                )
            
            # If we're starting before working hours on the same day, move to working hours
            if current_day.date() == start_dt.date() and current_day.hour < working_hours[0]:
                current_day = current_day.replace(hour=working_hours[0])
            
            while current_day < end_dt:
                # Skip weekends (Saturday = 5, Sunday = 6)
                if current_day.weekday() >= 5:
                    current_day = (current_day + timedelta(days=1)).replace(
                        hour=working_hours[0], minute=0, second=0, microsecond=0
                    )
                    continue
                
                # Set end of working day
                end_of_day = current_day.replace(
                    hour=working_hours[1], minute=0, second=0, microsecond=0
                )
                
                while current_day + meeting_duration <= end_of_day:
                    slot_end = current_day + meeting_duration
                    
                    # Check if this slot overlaps with any busy slot
                    is_available = True
                    for busy_start, busy_end in busy_slots:
                        if (current_day < busy_end and slot_end > busy_start):
                            is_available = False
                            # Jump to the end of the busy period
                            current_day = busy_end
                            break
                    
                    if is_available:
                        available_slots.append({
                            'start': current_day.isoformat(),
                            'end': slot_end.isoformat()
                        })
                        # Move to the next slot
                        current_day += timedelta(minutes=30)  # 30-minute increments
                    
                    # If we've added enough slots, return
                    if len(available_slots) >= 10:  # Limit to 10 suggestions
                        return available_slots
                
                # Move to the next day
                current_day = (current_day.date() + timedelta(days=1)).replace(
                    hour=working_hours[0], minute=0, second=0, microsecond=0,
                    tzinfo=current_day.tzinfo
                )
            
            return available_slots
        
        except HttpError as error:
            logger.error(f"Error suggesting meeting times: {error}")
            raise 