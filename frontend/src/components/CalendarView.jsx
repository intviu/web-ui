import React, { useState, useEffect } from 'react';
import {
  Box, Typography, Paper, Grid, 
  Card, CardContent, CircularProgress,
  Button, Chip, Dialog, DialogTitle,
  DialogContent, DialogActions, TextField,
  Divider, List, ListItem, ListItemText,
  IconButton, Tooltip
} from '@mui/material';
import { styled } from '@mui/material/styles';
import RefreshIcon from '@mui/icons-material/Refresh';
import DateRangeIcon from '@mui/icons-material/DateRange';
import ScheduleIcon from '@mui/icons-material/Schedule';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import PeopleIcon from '@mui/icons-material/People';
import MoreTimeIcon from '@mui/icons-material/MoreTime';
import AccessTimeFilledIcon from '@mui/icons-material/AccessTimeFilled';

// Styled components
const CalendarContainer = styled(Box)(({ theme }) => ({
  padding: theme.spacing(3),
}));

const EventCard = styled(Card)(({ theme, hasConflict }) => ({
  marginBottom: theme.spacing(2),
  borderLeft: hasConflict ? `4px solid ${theme.palette.error.main}` : 'none',
}));

const NoEventsMessage = styled(Typography)(({ theme }) => ({
  textAlign: 'center',
  padding: theme.spacing(4),
  color: theme.palette.text.secondary,
}));

const SectionTitle = styled(Typography)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  fontWeight: 600,
}));

const TimeSlotItem = styled(ListItem)(({ theme, isSelected }) => ({
  cursor: 'pointer',
  backgroundColor: isSelected ? theme.palette.action.selected : 'transparent',
  '&:hover': {
    backgroundColor: theme.palette.action.hover,
  },
}));

// CalendarView Component
const CalendarView = ({ isAuthenticated }) => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [daysToShow, setDaysToShow] = useState(7);
  
  // State for availability check
  const [availabilityDialog, setAvailabilityDialog] = useState(false);
  const [meetingDate, setMeetingDate] = useState('');
  const [meetingTime, setMeetingTime] = useState('');
  const [duration, setDuration] = useState(30);
  const [checkingAvailability, setCheckingAvailability] = useState(false);
  const [availabilityResult, setAvailabilityResult] = useState(null);
  
  // State for suggesting meeting times
  const [suggestDialog, setSuggestDialog] = useState(false);
  const [suggestedTimes, setSuggestedTimes] = useState([]);
  const [loadingSuggestions, setLoadingSuggestions] = useState(false);
  const [selectedTimeSlot, setSelectedTimeSlot] = useState(null);
  
  // Format date for display
  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleString();
  };
  
  // Format date to ISO string for API
  const formatDateForApi = (date, time) => {
    if (!date) return '';
    // Create date object from inputs
    const dateObj = new Date(`${date}T${time || '00:00'}`);
    return dateObj.toISOString();
  };
  
  // Fetch calendar events
  const fetchEvents = async () => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`http://localhost:8001/api/calendar/events?days=${daysToShow}`, {
        credentials: 'include'
      });
      const data = await response.json();
      
      if (data.success) {
        setEvents(data.events || []);
      } else {
        setError(data.error || 'Failed to fetch calendar events');
      }
    } catch (error) {
      setError(`Error fetching calendar events: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };
  
  // Check availability for a time slot
  const checkAvailability = async () => {
    if (!meetingDate || !meetingTime) {
      setError('Please select both date and time');
      return;
    }
    
    setCheckingAvailability(true);
    setAvailabilityResult(null);
    
    try {
      const meetingDateTime = formatDateForApi(meetingDate, meetingTime);
      
      const response = await fetch('http://localhost:8001/api/calendar/availability', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          meetingDate: meetingDateTime,
          durationMinutes: duration,
        }),
      });
      
      const data = await response.json();
      setAvailabilityResult(data);
    } catch (error) {
      setError(`Error checking availability: ${error.message}`);
    } finally {
      setCheckingAvailability(false);
    }
  };
  
  // Get meeting time suggestions
  const getSuggestedTimes = async () => {
    setLoadingSuggestions(true);
    setSuggestedTimes([]);
    setSelectedTimeSlot(null);
    
    try {
      const response = await fetch('http://localhost:8001/api/calendar/suggest', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          daysAhead: daysToShow,
          durationMinutes: duration,
        }),
      });
      
      const data = await response.json();
      
      if (data.success) {
        setSuggestedTimes(data.suggested_times || []);
      } else {
        setError(data.error || 'Failed to get meeting suggestions');
      }
    } catch (error) {
      setError(`Error getting meeting suggestions: ${error.message}`);
    } finally {
      setLoadingSuggestions(false);
    }
  };
  
  // Handle availability dialog open/close
  const handleAvailabilityDialog = () => {
    setAvailabilityDialog(!availabilityDialog);
    if (!availabilityDialog) {
      // Reset form when opening
      setMeetingDate('');
      setMeetingTime('');
      setDuration(30);
      setAvailabilityResult(null);
    }
  };
  
  // Handle suggest dialog open/close
  const handleSuggestDialog = () => {
    setSuggestDialog(!suggestDialog);
    if (!suggestDialog) {
      // Get suggestions when opening
      getSuggestedTimes();
    }
  };
  
  // Handle time slot selection
  const handleTimeSlotSelect = (index) => {
    setSelectedTimeSlot(index);
  };
  
  // Use selected time slot
  const useSelectedTimeSlot = () => {
    if (selectedTimeSlot === null) return;
    
    const selected = suggestedTimes[selectedTimeSlot];
    if (!selected) return;
    
    // Extract date and time from the selected time slot
    const startDate = new Date(selected.start);
    
    // Format for input fields
    const formattedDate = startDate.toISOString().split('T')[0];
    const formattedTime = startDate.toISOString().split('T')[1].substring(0, 5);
    
    // Set in availability dialog
    setMeetingDate(formattedDate);
    setMeetingTime(formattedTime);
    
    // Close suggest dialog and open availability dialog
    setSuggestDialog(false);
    setAvailabilityDialog(true);
  };
  
  // Load events when component mounts
  useEffect(() => {
    if (isAuthenticated) {
      fetchEvents();
    }
  }, [isAuthenticated, daysToShow]);
  
  return (
    <CalendarContainer>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <SectionTitle variant="h5">Calendar Events</SectionTitle>
        <Box>
          <Tooltip title="Check availability for a specific time">
            <Button 
              variant="outlined" 
              startIcon={<AccessTimeFilledIcon />}
              onClick={handleAvailabilityDialog}
              sx={{ mr: 2 }}
            >
              Check Availability
            </Button>
          </Tooltip>
          
          <Tooltip title="Get suggested meeting times">
            <Button 
              variant="outlined" 
              startIcon={<MoreTimeIcon />}
              onClick={handleSuggestDialog}
              sx={{ mr: 2 }}
            >
              Suggest Times
            </Button>
          </Tooltip>
          
          <Tooltip title="Refresh calendar events">
            <IconButton onClick={fetchEvents} disabled={loading}>
              <RefreshIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>
      
      {/* Days selector */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle1" gutterBottom>
          Show events for next:
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          {[1, 3, 7, 14, 30].map((days) => (
            <Chip 
              key={days}
              label={`${days} day${days > 1 ? 's' : ''}`}
              onClick={() => setDaysToShow(days)}
              color={days === daysToShow ? "primary" : "default"}
            />
          ))}
        </Box>
      </Box>
      
      {/* Error message */}
      {error && (
        <Paper sx={{ p: 2, mb: 3, bgcolor: 'error.light' }}>
          <Typography color="error">{error}</Typography>
        </Paper>
      )}
      
      {/* Loading indicator */}
      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      )}
      
      {/* Event list */}
      {!loading && events.length > 0 ? (
        <Grid container spacing={3}>
          {events.map((event) => (
            <Grid item xs={12} md={6} key={event.id}>
              <EventCard>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {event.summary || 'Untitled Event'}
                  </Typography>
                  
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <DateRangeIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="body2">
                      {formatDate(event.start?.dateTime || event.start?.date)}
                    </Typography>
                  </Box>
                  
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <ScheduleIcon sx={{ mr: 1, color: 'primary.main' }} />
                    <Typography variant="body2">
                      Until {formatDate(event.end?.dateTime || event.end?.date)}
                    </Typography>
                  </Box>
                  
                  {event.location && (
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                      <LocationOnIcon sx={{ mr: 1, color: 'primary.main' }} />
                      <Typography variant="body2">{event.location}</Typography>
                    </Box>
                  )}
                  
                  {event.attendees && event.attendees.length > 0 && (
                    <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 1 }}>
                      <PeopleIcon sx={{ mr: 1, mt: 0.5, color: 'primary.main' }} />
                      <Box>
                        <Typography variant="body2" gutterBottom>
                          {event.attendees.length} attendee{event.attendees.length !== 1 ? 's' : ''}
                        </Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                          {event.attendees.slice(0, 5).map((attendee, index) => (
                            <Chip 
                              key={index} 
                              size="small" 
                              label={attendee.email || attendee.displayName} 
                              variant={attendee.responseStatus === 'accepted' ? 'filled' : 'outlined'}
                            />
                          ))}
                          {event.attendees.length > 5 && (
                            <Chip 
                              size="small" 
                              label={`+${event.attendees.length - 5} more`} 
                              variant="outlined"
                            />
                          )}
                        </Box>
                      </Box>
                    </Box>
                  )}
                  
                  {event.description && (
                    <>
                      <Divider sx={{ my: 1 }} />
                      <Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
                        {event.description}
                      </Typography>
                    </>
                  )}
                </CardContent>
              </EventCard>
            </Grid>
          ))}
        </Grid>
      ) : !loading && (
        <NoEventsMessage variant="body1">
          No events found for the selected time period
        </NoEventsMessage>
      )}
      
      {/* Check Availability Dialog */}
      <Dialog 
        open={availabilityDialog} 
        onClose={handleAvailabilityDialog}
        fullWidth
        maxWidth="sm"
      >
        <DialogTitle>Check Calendar Availability</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Meeting Date"
                  type="date"
                  fullWidth
                  InputLabelProps={{ shrink: true }}
                  value={meetingDate}
                  onChange={(e) => setMeetingDate(e.target.value)}
                  required
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="Meeting Time"
                  type="time"
                  fullWidth
                  InputLabelProps={{ shrink: true }}
                  value={meetingTime}
                  onChange={(e) => setMeetingTime(e.target.value)}
                  required
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Duration (minutes)"
                  type="number"
                  fullWidth
                  value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))}
                  inputProps={{ min: 15, step: 15 }}
                  margin="normal"
                />
              </Grid>
            </Grid>
            
            {/* Availability check results */}
            {availabilityResult && (
              <Box sx={{ mt: 3 }}>
                <Divider sx={{ mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  Result:
                </Typography>
                
                {availabilityResult.available ? (
                  <Box sx={{ p: 2, bgcolor: 'success.light', borderRadius: 1 }}>
                    <Typography variant="body1" sx={{ color: 'success.dark' }}>
                      ✓ You're available at this time!
                    </Typography>
                  </Box>
                ) : (
                  <Box sx={{ p: 2, bgcolor: 'error.light', borderRadius: 1 }}>
                    <Typography variant="body1" sx={{ color: 'error.dark' }}>
                      ✗ You have conflicts with this time
                    </Typography>
                    
                    {availabilityResult.conflicts.length > 0 && (
                      <>
                        <Typography variant="subtitle2" sx={{ mt: 1, mb: 0.5 }}>
                          Conflicting events:
                        </Typography>
                        <List dense disablePadding>
                          {availabilityResult.conflicts.map((conflict, index) => (
                            <ListItem key={index} disablePadding sx={{ py: 0.5 }}>
                              <ListItemText
                                primary={conflict.summary || 'Untitled event'}
                                secondary={`${formatDate(conflict.start?.dateTime)} - ${formatDate(conflict.end?.dateTime)}`}
                              />
                            </ListItem>
                          ))}
                        </List>
                      </>
                    )}
                  </Box>
                )}
              </Box>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleAvailabilityDialog}>Cancel</Button>
          <Button 
            variant="contained" 
            onClick={checkAvailability}
            disabled={checkingAvailability}
            startIcon={checkingAvailability ? <CircularProgress size={20} /> : null}
          >
            {checkingAvailability ? 'Checking...' : 'Check Availability'}
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Suggest Meeting Times Dialog */}
      <Dialog
        open={suggestDialog}
        onClose={handleSuggestDialog}
        fullWidth
        maxWidth="sm"
      >
        <DialogTitle>Suggested Meeting Times</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <Grid container spacing={2} sx={{ mb: 2 }}>
              <Grid item xs={12}>
                <TextField
                  label="Duration (minutes)"
                  type="number"
                  fullWidth
                  value={duration}
                  onChange={(e) => setDuration(Number(e.target.value))}
                  inputProps={{ min: 15, step: 15 }}
                  margin="normal"
                />
              </Grid>
            </Grid>
            
            {loadingSuggestions ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                <CircularProgress />
              </Box>
            ) : suggestedTimes.length > 0 ? (
              <List sx={{ maxHeight: 400, overflow: 'auto' }}>
                {suggestedTimes.map((timeSlot, index) => (
                  <TimeSlotItem
                    key={index}
                    isSelected={selectedTimeSlot === index}
                    onClick={() => handleTimeSlotSelect(index)}
                    divider
                  >
                    <ListItemText
                      primary={
                        <Typography variant="subtitle1">
                          {new Date(timeSlot.start).toLocaleDateString(undefined, { 
                            weekday: 'long', 
                            month: 'long', 
                            day: 'numeric' 
                          })}
                        </Typography>
                      }
                      secondary={
                        <>
                          <Typography variant="body2" component="span">
                            {new Date(timeSlot.start).toLocaleTimeString(undefined, { 
                              hour: '2-digit', 
                              minute: '2-digit' 
                            })}
                            {' - '}
                            {new Date(timeSlot.end).toLocaleTimeString(undefined, { 
                              hour: '2-digit', 
                              minute: '2-digit' 
                            })}
                          </Typography>
                        </>
                      }
                    />
                  </TimeSlotItem>
                ))}
              </List>
            ) : (
              <NoEventsMessage variant="body1">
                No available time slots found
              </NoEventsMessage>
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleSuggestDialog}>Cancel</Button>
          <Button onClick={getSuggestedTimes} disabled={loadingSuggestions}>
            Refresh
          </Button>
          <Button 
            variant="contained" 
            onClick={useSelectedTimeSlot}
            disabled={selectedTimeSlot === null}
          >
            Use Selected Time
          </Button>
        </DialogActions>
      </Dialog>
    </CalendarContainer>
  );
};

export default CalendarView; 