import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  CircularProgress,
  Button,
  List,
  ListItem,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from '@mui/material';

interface CalendarEvent {
  id: string;
  title: string;
  start: string;
  end: string;
  description?: string;
}

interface AvailabilitySlot {
  start: string;
  end: string;
}

const calendarApiService = {
  async getEvents(days: number = 7): Promise<CalendarEvent[]> {
    const response = await fetch(`http://localhost:8001/api/calendar/events?days=${days}`, {
      credentials: 'include'
    });
    return response.json();
  },

  async checkAvailability(date: string, duration: number): Promise<AvailabilitySlot[]> {
    const response = await fetch('http://localhost:8001/api/calendar/availability', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ date, duration }),
    });
    return response.json();
  },

  async suggestMeetingTimes(daysAhead: number, duration: number): Promise<AvailabilitySlot[]> {
    const response = await fetch('http://localhost:8001/api/calendar/suggest', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ daysAhead, duration }),
    });
    return response.json();
  },
};

export default function CalendarView() {
  const [events, setEvents] = useState<CalendarEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [availabilityDialogOpen, setAvailabilityDialogOpen] = useState(false);
  const [suggestDialogOpen, setSuggestDialogOpen] = useState(false);
  const [availabilityDate, setAvailabilityDate] = useState('');
  const [duration, setDuration] = useState(30);
  const [availableSlots, setAvailableSlots] = useState<AvailabilitySlot[]>([]);
  const [daysAhead, setDaysAhead] = useState(7);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const fetchedEvents = await calendarApiService.getEvents();
      setEvents(fetchedEvents);
    } catch (error) {
      console.error('Error fetching events:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCheckAvailability = async () => {
    try {
      const slots = await calendarApiService.checkAvailability(availabilityDate, duration);
      setAvailableSlots(slots);
    } catch (error) {
      console.error('Error checking availability:', error);
    }
  };

  const handleSuggestTimes = async () => {
    try {
      const slots = await calendarApiService.suggestMeetingTimes(daysAhead, duration);
      setAvailableSlots(slots);
    } catch (error) {
      console.error('Error suggesting meeting times:', error);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
      <Box sx={{ display: 'flex', gap: 2 }}>
        <Button
          variant="contained"
          color="primary"
          onClick={() => setAvailabilityDialogOpen(true)}
        >
          Check Availability
        </Button>
        <Button
          variant="contained"
          color="primary"
          onClick={() => setSuggestDialogOpen(true)}
        >
          Suggest Meeting Times
        </Button>
      </Box>

      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" gutterBottom>
          Upcoming Events
        </Typography>
        <List>
          {events.map((event) => (
            <ListItem key={event.id}>
              <ListItemText
                primary={event.title}
                secondary={`${new Date(event.start).toLocaleString()} - ${new Date(
                  event.end
                ).toLocaleString()}`}
              />
            </ListItem>
          ))}
        </List>
      </Paper>

      <Dialog open={availabilityDialogOpen} onClose={() => setAvailabilityDialogOpen(false)}>
        <DialogTitle>Check Availability</DialogTitle>
        <DialogContent>
          <TextField
            type="date"
            label="Date"
            fullWidth
            margin="normal"
            value={availabilityDate}
            onChange={(e) => setAvailabilityDate(e.target.value)}
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            type="number"
            label="Duration (minutes)"
            fullWidth
            margin="normal"
            value={duration}
            onChange={(e) => setDuration(Number(e.target.value))}
          />
          {availableSlots.length > 0 && (
            <List>
              {availableSlots.map((slot, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={`${new Date(slot.start).toLocaleString()} - ${new Date(
                      slot.end
                    ).toLocaleString()}`}
                  />
                </ListItem>
              ))}
            </List>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAvailabilityDialogOpen(false)}>Close</Button>
          <Button onClick={handleCheckAvailability} color="primary">
            Check
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={suggestDialogOpen} onClose={() => setSuggestDialogOpen(false)}>
        <DialogTitle>Suggest Meeting Times</DialogTitle>
        <DialogContent>
          <TextField
            type="number"
            label="Days Ahead"
            fullWidth
            margin="normal"
            value={daysAhead}
            onChange={(e) => setDaysAhead(Number(e.target.value))}
          />
          <TextField
            type="number"
            label="Duration (minutes)"
            fullWidth
            margin="normal"
            value={duration}
            onChange={(e) => setDuration(Number(e.target.value))}
          />
          {availableSlots.length > 0 && (
            <List>
              {availableSlots.map((slot, index) => (
                <ListItem key={index}>
                  <ListItemText
                    primary={`${new Date(slot.start).toLocaleString()} - ${new Date(
                      slot.end
                    ).toLocaleString()}`}
                  />
                </ListItem>
              ))}
            </List>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSuggestDialogOpen(false)}>Close</Button>
          <Button onClick={handleSuggestTimes} color="primary">
            Suggest
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
} 