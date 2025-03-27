import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { 
  AppBar, Toolbar, Typography, Button, Container, Box, IconButton, 
  Drawer, List, ListItem, ListItemIcon, ListItemText, Divider, 
  CssBaseline, CircularProgress, Paper
} from '@mui/material';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';
import EmailIcon from '@mui/icons-material/Email';
import CalendarMonthIcon from '@mui/icons-material/CalendarMonth';
import DashboardIcon from '@mui/icons-material/Dashboard';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';

// Import components
import EmailDashboard from './components/EmailDashboard';
import CalendarView from './components/CalendarView';
import GoogleAuthCallbackPage from './pages/GoogleAuthCallbackPage';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

// Styled components
const MainContent = styled('main')(({ theme }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
  height: '100vh',
  overflow: 'auto',
  backgroundColor: theme.palette.background.default,
}));

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
  justifyContent: 'center',
}));

const StyledLink = styled(Link)(({ theme }) => ({
  textDecoration: 'none',
  color: 'inherit',
  width: '100%',
}));

function App() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const [loading, setLoading] = useState(true);
  
  // Check authentication status on app load
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const response = await fetch('http://localhost:8001/api/auth/user', {
          credentials: 'include'
        });
        const data = await response.json();
        
        if (data.authenticated) {
          setIsAuthenticated(true);
          setUserEmail(data.email);
        } else {
          setIsAuthenticated(false);
          setUserEmail('');
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };
    
    checkAuthStatus();
  }, []);
  
  // Toggle drawer
  const toggleDrawer = () => {
    setIsDrawerOpen(!isDrawerOpen);
  };
  
  // Render loading screen
  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '100vh',
          flexDirection: 'column'
        }}>
          <CircularProgress size={60} />
          <Typography variant="h6" sx={{ mt: 2 }}>
            Loading application...
          </Typography>
        </Box>
      </ThemeProvider>
    );
  }
  
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Box sx={{ display: 'flex' }}>
          <CssBaseline />
          
          {/* App Bar */}
          <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            <Toolbar>
              <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={toggleDrawer}
                sx={{ mr: 2 }}
              >
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
                Virtual Business Manager
              </Typography>
              {isAuthenticated && (
                <Typography variant="body2" sx={{ mr: 2 }}>
                  {userEmail}
                </Typography>
              )}
            </Toolbar>
          </AppBar>
          
          {/* Side Drawer */}
          <Drawer
            variant="temporary"
            open={isDrawerOpen}
            onClose={toggleDrawer}
            sx={{
              width: 240,
              flexShrink: 0,
              '& .MuiDrawer-paper': {
                width: 240,
                boxSizing: 'border-box',
              },
            }}
          >
            <Toolbar />
            <Box sx={{ overflow: 'auto' }}>
              <DrawerHeader>
                <Typography variant="h6" color="primary">
                  Navigation
                </Typography>
              </DrawerHeader>
              <Divider />
              <List>
                <StyledLink to="/">
                  <ListItem button onClick={toggleDrawer}>
                    <ListItemIcon>
                      <DashboardIcon />
                    </ListItemIcon>
                    <ListItemText primary="Dashboard" />
                  </ListItem>
                </StyledLink>
                <StyledLink to="/email">
                  <ListItem button onClick={toggleDrawer}>
                    <ListItemIcon>
                      <EmailIcon />
                    </ListItemIcon>
                    <ListItemText primary="Email" />
                  </ListItem>
                </StyledLink>
                <StyledLink to="/calendar">
                  <ListItem button onClick={toggleDrawer}>
                    <ListItemIcon>
                      <CalendarMonthIcon />
                    </ListItemIcon>
                    <ListItemText primary="Calendar" />
                  </ListItem>
                </StyledLink>
              </List>
              <Divider />
              <List>
                <StyledLink to="/settings">
                  <ListItem button onClick={toggleDrawer}>
                    <ListItemIcon>
                      <SettingsIcon />
                    </ListItemIcon>
                    <ListItemText primary="Settings" />
                  </ListItem>
                </StyledLink>
                <ListItem button onClick={async () => {
                  await fetch('http://localhost:8001/api/auth/logout', {
                    method: 'POST',
                    credentials: 'include'
                  });
                  setIsAuthenticated(false);
                  setUserEmail('');
                  toggleDrawer();
                  window.location.href = '/';
                }}>
                  <ListItemIcon>
                    <LogoutIcon />
                  </ListItemIcon>
                  <ListItemText primary="Logout" />
                </ListItem>
              </List>
            </Box>
          </Drawer>
          
          {/* Main Content */}
          <MainContent>
            <Toolbar /> {/* Add spacing for the app bar */}
            <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
              <Routes>
                <Route path="/" element={
                  <Box sx={{ textAlign: 'center', mt: 4 }}>
                    <Typography variant="h4" gutterBottom>
                      Welcome to Virtual Business Manager
                    </Typography>
                    <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
                      <Typography variant="h6" gutterBottom>
                        Get Started
                      </Typography>
                      <Typography paragraph>
                        Use the menu to navigate to different features:
                      </Typography>
                      <Box sx={{ 
                        display: 'flex', 
                        justifyContent: 'center', 
                        flexWrap: 'wrap',
                        gap: 2,
                        mt: 3
                      }}>
                        <Button 
                          variant="contained" 
                          startIcon={<EmailIcon />}
                          component={Link}
                          to="/email"
                          size="large"
                        >
                          Email Dashboard
                        </Button>
                        <Button 
                          variant="contained" 
                          startIcon={<CalendarMonthIcon />}
                          component={Link}
                          to="/calendar"
                          size="large"
                        >
                          Calendar
                        </Button>
                      </Box>
                    </Paper>
                  </Box>
                } />
                <Route path="/email" element={<EmailDashboard />} />
                <Route path="/calendar" element={<CalendarView isAuthenticated={isAuthenticated} />} />
                <Route path="/auth/google/callback" element={<GoogleAuthCallbackPage />} />
                <Route path="/settings" element={
                  <Box sx={{ mt: 4 }}>
                    <Typography variant="h4" gutterBottom>
                      Settings
                    </Typography>
                    <Typography>
                      Settings page is under construction.
                    </Typography>
                  </Box>
                } />
              </Routes>
            </Container>
          </MainContent>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App; 