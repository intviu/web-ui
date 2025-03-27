import React, { useState, useEffect } from 'react';
import { Button, CircularProgress, Typography, Box, Alert } from '@mui/material';
import GoogleIcon from '@mui/icons-material/Google';

/**
 * Google Authentication Button component
 * 
 * @param {Object} props Component props
 * @param {Function} props.onAuthSuccess Callback function when authentication is successful
 * @param {Function} props.onAuthFailure Callback function when authentication fails
 * @returns {JSX.Element} The Google Auth Button component
 */
const GoogleAuthButton = ({ onAuthSuccess, onAuthFailure }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState(null);

  useEffect(() => {
    // Check if user is already authenticated
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/auth/user', {
        credentials: 'include'
      });
      const data = await response.json();
      
      if (data.authenticated) {
        setAuthenticated(true);
        setUserEmail(data.email);
        if (onAuthSuccess) {
          onAuthSuccess(data.email);
        }
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
    }
  };

  const handleLoginClick = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Get the auth URL from the server
      const response = await fetch('http://localhost:8001/api/auth/google/login', {
        credentials: 'include'
      });
      const data = await response.json();
      
      // Open the Google auth URL in a new window
      window.location.href = data.auth_url;
    } catch (error) {
      console.error('Error starting Google auth:', error);
      setError('Failed to start Google authentication');
      if (onAuthFailure) {
        onAuthFailure(error);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogoutClick = async () => {
    try {
      setLoading(true);
      
      // Call logout endpoint
      await fetch('http://localhost:8001/api/auth/logout', {
        method: 'POST',
        credentials: 'include'
      });
      
      setAuthenticated(false);
      setUserEmail(null);
      
      // Reload the page to clear any user state
      window.location.reload();
    } catch (error) {
      console.error('Error logging out:', error);
      setError('Failed to log out');
    } finally {
      setLoading(false);
    }
  };

  if (authenticated) {
    return (
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1 }}>
        <Typography variant="body2">
          Signed in as: {userEmail}
        </Typography>
        <Button
          variant="outlined"
          color="secondary"
          onClick={handleLogoutClick}
          disabled={loading}
          startIcon={loading ? <CircularProgress size={20} /> : null}
        >
          Sign Out
        </Button>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
      {error && (
        <Alert severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      )}
      
      <Button
        variant="contained"
        color="primary"
        onClick={handleLoginClick}
        disabled={loading}
        startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <GoogleIcon />}
        sx={{ textTransform: 'none' }}
      >
        Sign in with Google
      </Button>
      
      <Typography variant="caption" color="textSecondary" align="center">
        This will authorize access to your Gmail and Google Calendar
      </Typography>
    </Box>
  );
};

export default GoogleAuthButton; 