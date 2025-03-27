import React from 'react';
import {
  Box,
  VStack,
  Heading,
  Text,
  FormControl,
  FormLabel,
  Input,
  Switch,
  Button,
  Select,
  Divider,
  useColorModeValue,
  HStack,
  Avatar,
  IconButton,
} from '@chakra-ui/react';
import { FiUpload, FiSave, FiUser, FiBell, FiLock, FiGlobe } from 'react-icons/fi';

const Settings = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  return (
    <Box p={6}>
      <VStack spacing={8} align="stretch">
        <Heading size="lg">Settings</Heading>

        {/* Profile Settings */}
        <Box bg={bgColor} p={6} borderRadius="lg" border="1px" borderColor={borderColor}>
          <HStack spacing={4} mb={6}>
            <Avatar size="xl" name="John Smith" />
            <VStack align="start" spacing={1}>
              <Text fontSize="lg" fontWeight="bold">John Smith</Text>
              <Text color="gray.600">john.smith@example.com</Text>
            </VStack>
            <IconButton
              aria-label="Upload photo"
              icon={<FiUpload />}
              variant="outline"
              ml="auto"
            />
          </HStack>

          <VStack spacing={4} align="stretch">
            <FormControl>
              <FormLabel>Display Name</FormLabel>
              <Input defaultValue="John Smith" />
            </FormControl>
            <FormControl>
              <FormLabel>Email</FormLabel>
              <Input defaultValue="john.smith@example.com" />
            </FormControl>
            <FormControl>
              <FormLabel>Phone</FormLabel>
              <Input defaultValue="+1 (555) 123-4567" />
            </FormControl>
          </VStack>
        </Box>

        {/* Notification Settings */}
        <Box bg={bgColor} p={6} borderRadius="lg" border="1px" borderColor={borderColor}>
          <HStack mb={6}>
            <Icon as={FiBell} />
            <Heading size="md">Notification Settings</Heading>
          </HStack>

          <VStack spacing={4} align="stretch">
            <FormControl display="flex" alignItems="center">
              <FormLabel mb="0">Email Notifications</FormLabel>
              <Switch defaultChecked />
            </FormControl>
            <FormControl display="flex" alignItems="center">
              <FormLabel mb="0">Push Notifications</FormLabel>
              <Switch defaultChecked />
            </FormControl>
            <FormControl display="flex" alignItems="center">
              <FormLabel mb="0">SMS Notifications</FormLabel>
              <Switch />
            </FormControl>
          </VStack>
        </Box>

        {/* Security Settings */}
        <Box bg={bgColor} p={6} borderRadius="lg" border="1px" borderColor={borderColor}>
          <HStack mb={6}>
            <Icon as={FiLock} />
            <Heading size="md">Security</Heading>
          </HStack>

          <VStack spacing={4} align="stretch">
            <FormControl>
              <FormLabel>Current Password</FormLabel>
              <Input type="password" />
            </FormControl>
            <FormControl>
              <FormLabel>New Password</FormLabel>
              <Input type="password" />
            </FormControl>
            <FormControl>
              <FormLabel>Confirm New Password</FormLabel>
              <Input type="password" />
            </FormControl>
            <FormControl display="flex" alignItems="center">
              <FormLabel mb="0">Two-Factor Authentication</FormLabel>
              <Switch />
            </FormControl>
          </VStack>
        </Box>

        {/* Preferences */}
        <Box bg={bgColor} p={6} borderRadius="lg" border="1px" borderColor={borderColor}>
          <HStack mb={6}>
            <Icon as={FiGlobe} />
            <Heading size="md">Preferences</Heading>
          </HStack>

          <VStack spacing={4} align="stretch">
            <FormControl>
              <FormLabel>Language</FormLabel>
              <Select defaultValue="en">
                <option value="en">English</option>
                <option value="es">Spanish</option>
                <option value="fr">French</option>
                <option value="de">German</option>
              </Select>
            </FormControl>
            <FormControl>
              <FormLabel>Time Zone</FormLabel>
              <Select defaultValue="utc">
                <option value="utc">UTC</option>
                <option value="est">Eastern Time</option>
                <option value="pst">Pacific Time</option>
              </Select>
            </FormControl>
            <FormControl display="flex" alignItems="center">
              <FormLabel mb="0">Dark Mode</FormLabel>
              <Switch />
            </FormControl>
          </VStack>
        </Box>

        {/* Save Button */}
        <Button leftIcon={<FiSave />} colorScheme="primary" size="lg">
          Save Changes
        </Button>
      </VStack>
    </Box>
  );
};

export default Settings; 