import { extendTheme } from '@chakra-ui/react';

const colors = {
  primary: {
    500: '#2D5BFF',
    600: '#244AD8',
  },
  secondary: {
    500: '#4A4A4A',
    600: '#363636',
  },
  success: {
    500: '#00C48C',
    600: '#00A376',
  },
  warning: {
    500: '#FFA26B',
    600: '#FF8A47',
  },
  error: {
    500: '#FF647C',
    600: '#FF4967',
  },
  background: {
    100: '#F7F9FC',
    200: '#EDF1F7',
  }
};

const fonts = {
  heading: 'Inter, sans-serif',
  body: 'Inter, sans-serif',
  mono: 'JetBrains Mono, monospace',
};

const components = {
  Card: {
    baseStyle: {
      container: {
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
        bg: 'white',
      }
    }
  },
  Button: {
    baseStyle: {
      borderRadius: '8px',
      fontWeight: 'semibold',
    },
    variants: {
      primary: {
        bg: 'primary.500',
        color: 'white',
        _hover: { bg: 'primary.600' },
      },
      secondary: {
        bg: 'secondary.500',
        color: 'white',
        _hover: { bg: 'secondary.600' },
      },
      success: {
        bg: 'success.500',
        color: 'white',
        _hover: { bg: 'success.600' },
      },
    }
  }
};

const breakpoints = {
  sm: '320px',
  md: '768px',
  lg: '1366px',
  xl: '1920px',
};

const theme = extendTheme({
  colors,
  fonts,
  components,
  breakpoints,
  styles: {
    global: {
      body: {
        bg: 'background.100',
        color: 'secondary.500',
      }
    }
  }
});

export default theme; 