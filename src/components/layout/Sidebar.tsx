import React from 'react';
import { Box, VStack, Icon, Text, Flex } from '@chakra-ui/react';
import { Link, useLocation } from 'react-router-dom';
import {
  FiHome,
  FiCalendar,
  FiUsers,
  FiDollarSign,
  FiShare2,
  FiBook,
  FiSettings
} from 'react-icons/fi';

interface NavItemProps {
  icon: any;
  children: string;
  to: string;
}

const NavItem: React.FC<NavItemProps> = ({ icon, children, to }) => {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <Link to={to}>
      <Flex
        align="center"
        p={3}
        mx={3}
        borderRadius="lg"
        role="group"
        cursor="pointer"
        bg={isActive ? 'primary.500' : 'transparent'}
        color={isActive ? 'white' : 'secondary.500'}
        _hover={{
          bg: isActive ? 'primary.600' : 'background.200',
        }}
      >
        <Icon
          mr={4}
          fontSize="16"
          as={icon}
        />
        <Text fontSize="sm" fontWeight="medium">
          {children}
        </Text>
      </Flex>
    </Link>
  );
};

const Sidebar = () => {
  return (
    <Box
      w={{ base: '70px', lg: '240px' }}
      h="100vh"
      bg="white"
      borderRight="1px"
      borderColor="background.200"
      position="sticky"
      top={0}
    >
      <VStack spacing={1} align="stretch" py={5}>
        <Box px={4} mb={8}>
          <Text fontSize="xl" fontWeight="bold" color="primary.500">
            TARA
          </Text>
        </Box>

        <NavItem icon={FiHome} to="/">
          Dashboard
        </NavItem>
        <NavItem icon={FiCalendar} to="/calendar">
          Calendar
        </NavItem>
        <NavItem icon={FiUsers} to="/clients">
          Clients
        </NavItem>
        <NavItem icon={FiDollarSign} to="/finance">
          Finance
        </NavItem>
        <NavItem icon={FiShare2} to="/social">
          Social Media
        </NavItem>
        <NavItem icon={FiBook} to="/knowledge">
          Knowledge Base
        </NavItem>
        <NavItem icon={FiSettings} to="/settings">
          Settings
        </NavItem>
      </VStack>
    </Box>
  );
};

export default Sidebar; 