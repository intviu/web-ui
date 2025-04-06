import React, { useState } from 'react';
import { Button, CircularProgress } from '@mui/material';
import GoogleIcon from '@mui/icons-material/Google';

interface GoogleAuthButtonProps {
  onAuthSuccess: (email: string) => void;
}

export default function GoogleAuthButton({ onAuthSuccess }: GoogleAuthButtonProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleLoginClick = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('http://localhost:8001/api/auth/google/login', {
        credentials: 'include'
      });
      const data = await response.json();
      window.location.href = data.auth_url;
    } catch (error) {
      console.error('Error during login:', error);
      setError('Failed to initiate login');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <Button
      variant="contained"
      color="primary"
      onClick={handleLoginClick}
      startIcon={<GoogleIcon />}
      disabled={loading}
    >
      Sign in with Google
    </Button>
  );
} 