import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Box, Typography, CircularProgress } from '@mui/material';

export default function GoogleAuthCallbackPage() {
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const processAuthCallback = async () => {
      try {
        const response = await fetch(
          `http://localhost:8001/api/auth/google/callback${location.search}`,
          {
            credentials: 'include'
          }
        );
        const data = await response.json();
        
        if (data.success) {
          // Redirect to the main page after successful authentication
          setTimeout(() => {
            navigate('/');
          }, 1000);
        } else {
          setError(data.error || 'Authentication failed');
        }
      } catch (error) {
        console.error('Error processing callback:', error);
        setError('Failed to process authentication');
      }
    };

    processAuthCallback();
  }, [navigate, location]);

  if (error) {
    return (
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        height="100vh"
      >
        <Typography color="error" variant="h6">
          {error}
        </Typography>
        <Typography variant="body1" sx={{ mt: 2 }}>
          Please try signing in again.
        </Typography>
      </Box>
    );
  }

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      height="100vh"
    >
      <CircularProgress />
      <Typography variant="h6" sx={{ mt: 2 }}>
        Processing authentication...
      </Typography>
    </Box>
  );
} 