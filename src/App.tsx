import React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import theme from './theme';
import MainLayout from './components/layout/MainLayout';

// Import pages
import Dashboard from './pages/Dashboard';
import Calendar from './pages/Calendar';
import Clients from './pages/Clients';
import Finance from './pages/Finance';
import Social from './pages/Social';
import Knowledge from './pages/Knowledge';
import Settings from './pages/Settings';

const App = () => {
  return (
    <ChakraProvider theme={theme}>
      <Router>
        <MainLayout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/calendar" element={<Calendar />} />
            <Route path="/clients" element={<Clients />} />
            <Route path="/finance" element={<Finance />} />
            <Route path="/social" element={<Social />} />
            <Route path="/knowledge" element={<Knowledge />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </MainLayout>
      </Router>
    </ChakraProvider>
  );
};

export default App; 