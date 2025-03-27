import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Container, Paper, Typography, CircularProgress, Box, Alert } from '@mui/material';

/**
 * Google Auth Callback Page
 * 
 * This page handles the OAuth2 callback from Google
 * It processes the authorization code and redirects the user
 */
const GoogleAuthCallbackPage = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [userEmail, setUserEmail] = useState(null);
  
  const location = useLocation();
  const navigate = useNavigate();
  
  useEffect(() => {
    const processAuthCallback = async () => {
      try {
        // Get the query parameters from the URL
        const params = new URLSearchParams(location.search);
        const code = params.get('code');
        const state = params.get('state');
        const error = params.get('error');
        
        if (error) {
          setError(`Authentication error: ${error}`);
          setLoading(false);
          return;
        }
        
        if (!code || !state) {
          setError('Missing authorization code or state');
          setLoading(false);
          return;
        }
        
        // Call the backend to process the authorization code
        // The backend will exchange the code for tokens and store them
        const response = await fetch(`http://localhost:8001/api/auth/google/callback${location.search}`, {
          credentials: 'include'
        });
        const data = await response.json();
        
        if (data.success) {
          setSuccess(true);
          setUserEmail(data.email);
          
          // Redirect to the main page after a short delay
          setTimeout(() => {
            navigate('/');
          }, 2000);
        } else {
          setError(data.error || 'Authentication failed');
        }
      } catch (err) {
        console.error('Error processing auth callback:', err);
        setError('Failed to process authentication. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    
    processAuthCallback();
  }, [location, navigate]);
  
  return (
    <Container maxWidth="sm" sx={{ mt: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h5" component="h1" gutterBottom align="center">
          Google Authentication
        </Typography>
        
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', my: 4 }}>
          {loading && (
            <>
              <CircularProgress />
              <Typography variant="body1" sx={{ mt: 2 }}>
                Processing authentication...
              </Typography>
            </>
          )}
          
          {!loading && error && (
            <Alert severity="error" sx={{ width: '100%', mb: 2 }}>
              {error}
            </Alert>
          )}
          
          {!loading && success && (
            <>
              <Alert severity="success" sx={{ width: '100%', mb: 2 }}>
                Successfully authenticated with Google!
              </Alert>
              <Typography variant="body1">
                Welcome, {userEmail}
              </Typography>
              <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                Redirecting you to the main page...
              </Typography>
            </>
          )}
        </Box>
      </Paper>
    </Container>
  );
};

export default GoogleAuthCallbackPage; 