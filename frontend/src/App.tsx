import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import {
  AppBar,
  Box,
  CssBaseline,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Container,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Mail as MailIcon,
  Event as EventIcon,
  ExitToApp as LogoutIcon,
} from '@mui/icons-material';
import EmailDashboard from './components/EmailDashboard';
import CalendarView from './components/CalendarView';
import GoogleAuthButton from './components/GoogleAuthButton';
import GoogleAuthCallbackPage from './pages/GoogleAuthCallbackPage';

const drawerWidth = 240;

function App() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState('');

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await fetch('http://localhost:8001/api/auth/user', {
        credentials: 'include'
      });
      const data = await response.json();
      setIsAuthenticated(data.authenticated);
      setUserEmail(data.email || '');
    } catch (error) {
      console.error('Error checking auth status:', error);
      setIsAuthenticated(false);
    }
  };

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <div>
      <Toolbar />
      <List>
        <ListItem button component="a" href="/email">
          <ListItemIcon>
            <MailIcon />
          </ListItemIcon>
          <ListItemText primary="Email" />
        </ListItem>
        <ListItem button component="a" href="/calendar">
          <ListItemIcon>
            <EventIcon />
          </ListItemIcon>
          <ListItemText primary="Calendar" />
        </ListItem>
      </List>
    </div>
  );

  if (!isAuthenticated) {
    return (
      <Container maxWidth="sm" sx={{ mt: 4, textAlign: 'center' }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Virtual Business Manager
        </Typography>
        <GoogleAuthButton
          onAuthSuccess={(email) => {
            setIsAuthenticated(true);
            setUserEmail(email);
          }}
        />
      </Container>
    );
  }

  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <AppBar
          position="fixed"
          sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}
        >
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2, display: { sm: 'none' } }}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
              Virtual Business Manager
            </Typography>
            <Typography variant="body1" sx={{ mr: 2 }}>
              {userEmail}
            </Typography>
            <IconButton
              color="inherit"
              onClick={async () => {
                await fetch('http://localhost:8001/api/auth/logout', {
                  method: 'POST',
                  credentials: 'include'
                });
                setIsAuthenticated(false);
                setUserEmail('');
              }}
            >
              <LogoutIcon />
            </IconButton>
          </Toolbar>
        </AppBar>
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
          open
        >
          {drawer}
        </Drawer>
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 3,
            width: { sm: `calc(100% - ${drawerWidth}px)` },
          }}
        >
          <Toolbar />
          <Routes>
            <Route path="/email" element={<EmailDashboard />} />
            <Route path="/calendar" element={<CalendarView />} />
            <Route path="/auth/google/callback" element={<GoogleAuthCallbackPage />} />
            <Route path="/" element={<Navigate to="/email" replace />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}

export default App;
