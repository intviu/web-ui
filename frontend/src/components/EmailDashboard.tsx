import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  List,
  ListItem,
  ListItemText,
  Typography,
  CircularProgress,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';

interface Email {
  id: string;
  subject: string;
  sender: string;
  timestamp: string;
  content?: string;
}

const emailApiService = {
  async getEmails(): Promise<Email[]> {
    const response = await fetch('http://localhost:8001/api/emails', {
      credentials: 'include'
    });
    return response.json();
  },

  async getEmail(emailId: string): Promise<Email> {
    const response = await fetch(`http://localhost:8001/api/emails/${emailId}`, {
      credentials: 'include'
    });
    return response.json();
  },

  async sendEmail(to: string, subject: string, content: string): Promise<void> {
    await fetch('http://localhost:8001/api/emails/send', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ to, subject, content }),
    });
  },
};

export default function EmailDashboard() {
  const [emails, setEmails] = useState<Email[]>([]);
  const [selectedEmail, setSelectedEmail] = useState<Email | null>(null);
  const [loading, setLoading] = useState(true);
  const [composeOpen, setComposeOpen] = useState(false);
  const [newEmail, setNewEmail] = useState({
    to: '',
    subject: '',
    content: '',
  });

  useEffect(() => {
    fetchEmails();
  }, []);

  const fetchEmails = async () => {
    try {
      const fetchedEmails = await emailApiService.getEmails();
      setEmails(fetchedEmails);
    } catch (error) {
      console.error('Error fetching emails:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEmailClick = async (email: Email) => {
    try {
      const fullEmail = await emailApiService.getEmail(email.id);
      setSelectedEmail(fullEmail);
    } catch (error) {
      console.error('Error fetching email details:', error);
    }
  };

  const handleSendEmail = async () => {
    try {
      await emailApiService.sendEmail(
        newEmail.to,
        newEmail.subject,
        newEmail.content
      );
      setComposeOpen(false);
      setNewEmail({ to: '', subject: '', content: '' });
      await fetchEmails();
    } catch (error) {
      console.error('Error sending email:', error);
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
    <Box sx={{ display: 'flex', height: 'calc(100vh - 100px)' }}>
      <Paper sx={{ width: 300, mr: 2, overflow: 'auto' }}>
        <Box sx={{ p: 2 }}>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            onClick={() => setComposeOpen(true)}
          >
            Compose
          </Button>
        </Box>
        <List>
          {emails.map((email) => (
            <ListItem
              button
              key={email.id}
              selected={selectedEmail?.id === email.id}
              onClick={() => handleEmailClick(email)}
            >
              <ListItemText
                primary={email.subject}
                secondary={`${email.sender} - ${new Date(
                  email.timestamp
                ).toLocaleString()}`}
              />
            </ListItem>
          ))}
        </List>
      </Paper>

      <Paper sx={{ flexGrow: 1, p: 2, overflow: 'auto' }}>
        {selectedEmail ? (
          <>
            <Typography variant="h6">{selectedEmail.subject}</Typography>
            <Typography variant="subtitle2" color="textSecondary">
              From: {selectedEmail.sender}
              <br />
              Date: {new Date(selectedEmail.timestamp).toLocaleString()}
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Typography>{selectedEmail.content}</Typography>
            </Box>
          </>
        ) : (
          <Typography variant="body1" color="textSecondary">
            Select an email to view its contents
          </Typography>
        )}
      </Paper>

      <Dialog open={composeOpen} onClose={() => setComposeOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Compose Email</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="To"
            fullWidth
            value={newEmail.to}
            onChange={(e) => setNewEmail({ ...newEmail, to: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Subject"
            fullWidth
            value={newEmail.subject}
            onChange={(e) => setNewEmail({ ...newEmail, subject: e.target.value })}
          />
          <TextField
            margin="dense"
            label="Content"
            multiline
            rows={4}
            fullWidth
            value={newEmail.content}
            onChange={(e) => setNewEmail({ ...newEmail, content: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setComposeOpen(false)}>Cancel</Button>
          <Button onClick={handleSendEmail} color="primary">
            Send
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
} 