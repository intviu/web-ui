import React from 'react';
import {
  Box,
  Flex,
  IconButton,
  Input,
  InputGroup,
  InputLeftElement,
  Avatar,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  Badge,
} from '@chakra-ui/react';
import {
  FiSearch,
  FiBell,
  FiPlus,
  FiUser,
  FiSettings,
  FiLogOut,
} from 'react-icons/fi';

const TopNav = () => {
  return (
    <Box
      as="nav"
      bg="white"
      px={6}
      py={4}
      borderBottom="1px"
      borderColor="background.200"
    >
      <Flex justify="space-between" align="center">
        {/* Search Bar */}
        <InputGroup maxW="400px">
          <InputLeftElement pointerEvents="none">
            <FiSearch color="gray.300" />
          </InputLeftElement>
          <Input
            placeholder="Search..."
            bg="background.100"
            border="none"
            _placeholder={{ color: 'gray.400' }}
            _focus={{ bg: 'white', boxShadow: 'sm' }}
          />
        </InputGroup>

        {/* Right Side Actions */}
        <Flex align="center" gap={4}>
          {/* Quick Action Button */}
          <IconButton
            aria-label="Quick actions"
            icon={<FiPlus />}
            variant="ghost"
            colorScheme="primary"
            fontSize="20px"
          />

          {/* Notifications */}
          <Box position="relative">
            <IconButton
              aria-label="Notifications"
              icon={<FiBell />}
              variant="ghost"
              fontSize="20px"
            />
            <Badge
              position="absolute"
              top="-1"
              right="-1"
              colorScheme="error"
              borderRadius="full"
              boxSize="5"
              display="flex"
              alignItems="center"
              justifyContent="center"
            >
              3
            </Badge>
          </Box>

          {/* User Menu */}
          <Menu>
            <MenuButton>
              <Avatar
                size="sm"
                name="User Name"
                src="https://bit.ly/broken-link"
                cursor="pointer"
              />
            </MenuButton>
            <MenuList>
              <MenuItem icon={<FiUser />}>Profile</MenuItem>
              <MenuItem icon={<FiSettings />}>Settings</MenuItem>
              <MenuItem icon={<FiLogOut />}>Logout</MenuItem>
            </MenuList>
          </Menu>
        </Flex>
      </Flex>
    </Box>
  );
};

export default TopNav; 