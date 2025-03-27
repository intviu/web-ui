import React, { useState, useEffect } from 'react';
import {
  Box, Container, Grid, Typography, Button, Card, CardContent, 
  List, ListItem, ListItemText, Divider, TextField, Tabs, Tab,
  Dialog, DialogTitle, DialogContent, DialogActions, Paper
} from '@mui/material';
import { styled } from '@mui/material/styles';
import EmailIcon from '@mui/icons-material/Email';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import RefreshIcon from '@mui/icons-material/Refresh';
import SendIcon from '@mui/icons-material/Send';
import DraftsIcon from '@mui/icons-material/Drafts';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import GoogleAuthButton from './GoogleAuthButton';

// API service for email operations
const emailApiService = {
  async getEmails(query = "is:inbox", maxResults = 10) {
    // This would be a fetch request to your backend
    const response = await fetch('http://localhost:8001/api/emails', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({ query, maxResults }),
    });
    return await response.json();
  },
  
  async getEmail(emailId) {
    const response = await fetch(`http://localhost:8001/api/emails/${emailId}`, {
      credentials: 'include'
    });
    return await response.json();
  },
  
  async sendEmail(emailData, isDraft = false) {
    const endpoint = isDraft ? '/api/emails/draft' : '/api/emails/send';
    const response = await fetch(`http://localhost:8001${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(emailData),
    });
    return await response.json();
  },
  
  async getCalendarEvents(days = 7) {
    const response = await fetch(`http://localhost:8001/api/calendar/events?days=${days}`, {
      credentials: 'include'
    });
    return await response.json();
  },
  
  async checkAvailability(meetingDate, durationMinutes = 30) {
    const response = await fetch('http://localhost:8001/api/calendar/availability', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({ meetingDate, durationMinutes }),
    });
    return await response.json();
  },
  
  async suggestMeetingTimes(daysAhead = 5, durationMinutes = 30) {
    const response = await fetch('http://localhost:8001/api/calendar/suggest', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({ daysAhead, durationMinutes }),
    });
    return await response.json();
  }
};

// Styled components
const SectionTitle = styled(Typography)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  fontWeight: 600,
}));

const EmailCard = styled(Card)(({ theme, selected }) => ({
  marginBottom: theme.spacing(1),
  cursor: 'pointer',
  transition: 'all 0.2s',
  border: selected ? `1px solid ${theme.palette.primary.main}` : 'none',
  '&:hover': {
    backgroundColor: theme.palette.action.hover,
  },
}));

const CalendarCard = styled(Card)(({ theme }) => ({
  marginBottom: theme.spacing(1),
}));

// Email Dashboard Component
const EmailDashboard = () => {
  const [tabValue, setTabValue] = useState(0);
  const [emails, setEmails] = useState([]);
  const [events, setEvents] = useState([]);
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [emailContent, setEmailContent] = useState(null);
  const [composeOpen, setComposeOpen] = useState(false);
  const [suggestDialogOpen, setSuggestDialogOpen] = useState(false);
  const [suggestedTimes, setSuggestedTimes] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authError, setAuthError] = useState(null);
  const [loading, setLoading] = useState({
    emails: false,
    calendar: false,
    emailContent: false,
    compose: false,
    suggest: false,
  });
  
  // Form states for compose email
  const [emailForm, setEmailForm] = useState({
    to: '',
    subject: '',
    body: '',
    cc: '',
    bcc: '',
  });
  
  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  // Fetch emails
  const fetchEmails = async () => {
    if (!isAuthenticated) return;
    
    try {
      setLoading({ ...loading, emails: true });
      const data = await emailApiService.getEmails();
      setEmails(data.emails || []);
    } catch (error) {
      console.error('Error fetching emails:', error);
    } finally {
      setLoading({ ...loading, emails: false });
    }
  };
  
  // Fetch calendar events
  const fetchCalendarEvents = async () => {
    if (!isAuthenticated) return;
    
    try {
      setLoading({ ...loading, calendar: true });
      const data = await emailApiService.getCalendarEvents();
      setEvents(data.events || []);
    } catch (error) {
      console.error('Error fetching calendar events:', error);
    } finally {
      setLoading({ ...loading, calendar: false });
    }
  };
  
  // Fetch email content
  const fetchEmailContent = async (emailId) => {
    if (!isAuthenticated) return;
    
    try {
      setLoading({ ...loading, emailContent: true });
      const data = await emailApiService.getEmail(emailId);
      setEmailContent(data.email || null);
    } catch (error) {
      console.error('Error fetching email content:', error);
    } finally {
      setLoading({ ...loading, emailContent: false });
    }
  };
  
  // Handle email selection
  const handleEmailSelect = (email) => {
    setSelectedEmail(email);
    fetchEmailContent(email.id);
  };
  
  // Handle compose email open/close
  const handleComposeToggle = () => {
    setComposeOpen(!composeOpen);
    if (!composeOpen) {
      // Reset form when opening
      setEmailForm({
        to: '',
        subject: '',
        body: '',
        cc: '',
        bcc: '',
      });
    }
  };
  
  // Handle form input change
  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setEmailForm({
      ...emailForm,
      [name]: value,
    });
  };
  
  // Handle send email
  const handleSendEmail = async (isDraft = false) => {
    try {
      setLoading({ ...loading, compose: true });
      const result = await emailApiService.sendEmail(emailForm, isDraft);
      if (result.result && result.result.success) {
        setComposeOpen(false);
        fetchEmails(); // Refresh emails after sending
      } else {
        alert(`Failed to ${isDraft ? 'save draft' : 'send email'}: ${result.result?.error || 'Unknown error'}`);
      }
    } catch (error) {
      console.error(`Error ${isDraft ? 'saving draft' : 'sending email'}:`, error);
    } finally {
      setLoading({ ...loading, compose: false });
    }
  };
  
  // Open suggest meeting times dialog
  const handleSuggestMeetingTimes = async () => {
    try {
      setSuggestDialogOpen(true);
      setLoading({ ...loading, suggest: true });
      const result = await emailApiService.suggestMeetingTimes();
      setSuggestedTimes(result.suggested_times || []);
    } catch (error) {
      console.error('Error suggesting meeting times:', error);
    } finally {
      setLoading({ ...loading, suggest: false });
    }
  };
  
  // Format date for display
  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown date';
    const date = new Date(dateString);
    return date.toLocaleString();
  };
  
  // Handle successful authentication
  const handleAuthSuccess = (userEmail) => {
    setIsAuthenticated(true);
    setAuthError(null);
    // Load data after authentication
    fetchEmails();
    fetchCalendarEvents();
  };
  
  // Handle authentication failure
  const handleAuthFailure = (error) => {
    setAuthError(`Authentication failed: ${error.message || 'Unknown error'}`);
    setIsAuthenticated(false);
  };
  
  // Load data on authentication change
  useEffect(() => {
    if (isAuthenticated) {
      fetchEmails();
      fetchCalendarEvents();
    }
  }, [isAuthenticated]);
  
  // Render authentication UI if not authenticated
  if (!isAuthenticated) {
    return (
      <Container maxWidth="sm">
        <Box sx={{ my: 8 }}>
          <Paper elevation={3} sx={{ p: 4 }}>
            <Typography variant="h4" component="h1" gutterBottom align="center">
              Email & Calendar Dashboard
            </Typography>
            
            <Typography variant="body1" paragraph align="center">
              Please sign in with your Google account to access your emails and calendar.
            </Typography>
            
            <Box sx={{ mt: 4 }}>
              <GoogleAuthButton 
                onAuthSuccess={handleAuthSuccess}
                onAuthFailure={handleAuthFailure}
              />
            </Box>
          </Paper>
        </Box>
      </Container>
    );
  }
  
  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Email & Calendar Dashboard
        </Typography>
        
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
          <GoogleAuthButton 
            onAuthSuccess={handleAuthSuccess}
            onAuthFailure={handleAuthFailure}
          />
        </Box>
        
        <Tabs value={tabValue} onChange={handleTabChange} sx={{ mb: 3 }}>
          <Tab icon={<EmailIcon />} label="Emails" />
          <Tab icon={<CalendarMonthIcon />} label="Calendar" />
        </Tabs>
        
        {/* Email Tab */}
        {tabValue === 0 && (
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <SectionTitle variant="h6">Inbox</SectionTitle>
                <Button 
                  startIcon={<RefreshIcon />} 
                  onClick={fetchEmails}
                  disabled={loading.emails}
                >
                  Refresh
                </Button>
              </Box>
              
              {loading.emails ? (
                <Typography>Loading emails...</Typography>
              ) : (
                <>
                  <Button 
                    variant="contained" 
                    startIcon={<EmailIcon />}
                    onClick={handleComposeToggle}
                    fullWidth
                    sx={{ mb: 2 }}
                  >
                    Compose Email
                  </Button>
                  
                  {emails.length > 0 ? (
                    emails.map((email) => (
                      <EmailCard 
                        key={email.id} 
                        selected={selectedEmail?.id === email.id}
                        onClick={() => handleEmailSelect(email)}
                      >
                        <CardContent>
                          <Typography variant="subtitle1" noWrap>
                            {email.subject || 'No subject'}
                          </Typography>
                          <Typography variant="body2" color="textSecondary" noWrap>
                            From: {email.sender || 'Unknown'}
                          </Typography>
                          <Typography variant="caption" color="textSecondary">
                            {formatDate(email.date)}
                          </Typography>
                        </CardContent>
                      </EmailCard>
                    ))
                  ) : (
                    <Typography>No emails found</Typography>
                  )}
                </>
              )}
            </Grid>
            
            <Grid item xs={12} md={8}>
              <SectionTitle variant="h6">Email Content</SectionTitle>
              
              {loading.emailContent ? (
                <Typography>Loading email content...</Typography>
              ) : emailContent ? (
                <Card>
                  <CardContent>
                    <Typography variant="h6">{emailContent.subject || 'No subject'}</Typography>
                    <Typography variant="body2" color="textSecondary">
                      From: {emailContent.sender || 'Unknown'} • {formatDate(emailContent.date)}
                    </Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                      To: {emailContent.to || 'Unknown'}
                      {emailContent.cc && ` • Cc: ${emailContent.cc}`}
                    </Typography>
                    <Divider sx={{ my: 2 }} />
                    <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>
                      {emailContent.body || 'No content'}
                    </Typography>
                  </CardContent>
                </Card>
              ) : (
                <Typography>Select an email to view its content</Typography>
              )}
            </Grid>
          </Grid>
        )}
        
        {/* Calendar Tab */}
        {tabValue === 1 && (
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <SectionTitle variant="h6">Upcoming Events</SectionTitle>
                <Box>
                  <Button 
                    startIcon={<RefreshIcon />} 
                    onClick={fetchCalendarEvents}
                    disabled={loading.calendar}
                    sx={{ mr: 1 }}
                  >
                    Refresh
                  </Button>
                  <Button 
                    variant="contained"
                    startIcon={<AccessTimeIcon />}
                    onClick={handleSuggestMeetingTimes}
                  >
                    Suggest Meeting Times
                  </Button>
                </Box>
              </Box>
              
              {loading.calendar ? (
                <Typography>Loading calendar events...</Typography>
              ) : events.length > 0 ? (
                events.map((event) => (
                  <CalendarCard key={event.id}>
                    <CardContent>
                      <Typography variant="h6">{event.summary || 'Untitled Event'}</Typography>
                      <Typography variant="body2" color="textSecondary">
                        {formatDate(event.start?.dateTime)} - {formatDate(event.end?.dateTime)}
                      </Typography>
                      {event.location && (
                        <Typography variant="body2">
                          Location: {event.location}
                        </Typography>
                      )}
                      {event.description && (
                        <Typography variant="body2" style={{ whiteSpace: 'pre-wrap' }}>
                          {event.description}
                        </Typography>
                      )}
                    </CardContent>
                  </CalendarCard>
                ))
              ) : (
                <Typography>No upcoming events found</Typography>
              )}
            </Grid>
            
            <Grid item xs={12} md={4}>
              <SectionTitle variant="h6">Calendar Summary</SectionTitle>
              <Card>
                <CardContent>
                  <Typography variant="body1">
                    You have {events.length} upcoming events in the next 7 days.
                  </Typography>
                  
                  {events.length > 0 && (
                    <>
                      <Typography variant="body2" sx={{ mt: 2, mb: 1 }}>
                        Next event:
                      </Typography>
                      <Typography variant="h6">
                        {events[0]?.summary || 'Untitled Event'}
                      </Typography>
                      <Typography variant="body2">
                        {formatDate(events[0]?.start?.dateTime)}
                      </Typography>
                    </>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
        
        {/* Compose Email Dialog */}
        <Dialog open={composeOpen} onClose={handleComposeToggle} fullWidth maxWidth="md">
          <DialogTitle>Compose Email</DialogTitle>
          <DialogContent>
            <TextField
              margin="normal"
              label="To"
              type="email"
              fullWidth
              variant="outlined"
              name="to"
              value={emailForm.to}
              onChange={handleFormChange}
            />
            <TextField
              margin="normal"
              label="Cc"
              type="email"
              fullWidth
              variant="outlined"
              name="cc"
              value={emailForm.cc}
              onChange={handleFormChange}
            />
            <TextField
              margin="normal"
              label="Bcc"
              type="email"
              fullWidth
              variant="outlined"
              name="bcc"
              value={emailForm.bcc}
              onChange={handleFormChange}
            />
            <TextField
              margin="normal"
              label="Subject"
              fullWidth
              variant="outlined"
              name="subject"
              value={emailForm.subject}
              onChange={handleFormChange}
            />
            <TextField
              margin="normal"
              label="Message"
              multiline
              rows={8}
              fullWidth
              variant="outlined"
              name="body"
              value={emailForm.body}
              onChange={handleFormChange}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleComposeToggle}>Cancel</Button>
            <Button 
              startIcon={<DraftsIcon />}
              onClick={() => handleSendEmail(true)}
              disabled={loading.compose}
            >
              Save as Draft
            </Button>
            <Button 
              variant="contained" 
              startIcon={<SendIcon />}
              onClick={() => handleSendEmail(false)}
              disabled={loading.compose}
            >
              Send
            </Button>
          </DialogActions>
        </Dialog>
        
        {/* Suggest Meeting Times Dialog */}
        <Dialog open={suggestDialogOpen} onClose={() => setSuggestDialogOpen(false)} fullWidth maxWidth="sm">
          <DialogTitle>Suggested Meeting Times</DialogTitle>
          <DialogContent>
            {loading.suggest ? (
              <Typography>Finding available times...</Typography>
            ) : suggestedTimes.length > 0 ? (
              <List>
                {suggestedTimes.map((timeSlot, index) => (
                  <ListItem key={index} divider={index < suggestedTimes.length - 1}>
                    <ListItemText
                      primary={formatDate(timeSlot.start)}
                      secondary={`to ${formatDate(timeSlot.end)}`}
                    />
                  </ListItem>
                ))}
              </List>
            ) : (
              <Typography>No available time slots found</Typography>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setSuggestDialogOpen(false)}>Close</Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
};

export default EmailDashboard; 