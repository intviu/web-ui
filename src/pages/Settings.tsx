import React from 'react';
import {
  Box,
  Grid,
  Heading,
  Text,
  VStack,
  HStack,
  Button,
  FormControl,
  FormLabel,
  Input,
  Switch,
  Select,
  useColorModeValue,
  Divider,
  Avatar,
  IconButton,
} from '@chakra-ui/react';
import { FiUpload, FiSave, FiLock, FiBell, FiUser } from 'react-icons/fi';

const Settings = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  return (
    <Box p={6}>
      <VStack spacing={8} align="stretch">
        <Heading size="lg">Settings</Heading>

        <Grid templateColumns="repeat(2, 1fr)" gap={8}>
          {/* Profile Settings */}
          <Box
            bg={bgColor}
            p={6}
            borderRadius="lg"
            border="1px"
            borderColor={borderColor}
          >
            <VStack spacing={6} align="start">
              <HStack>
                <Icon as={FiUser} />
                <Heading size="md">Profile Settings</Heading>
              </HStack>
              <VStack spacing={4} align="start" w="100%">
                <HStack spacing={4}>
                  <Avatar size="xl" name="John Doe" />
                  <Button leftIcon={<FiUpload />} variant="outline">
                    Change Photo
                  </Button>
                </HStack>
                <FormControl>
                  <FormLabel>Full Name</FormLabel>
                  <Input placeholder="John Doe" />
                </FormControl>
                <FormControl>
                  <FormLabel>Email</FormLabel>
                  <Input type="email" placeholder="john@example.com" />
                </FormControl>
                <FormControl>
                  <FormLabel>Phone</FormLabel>
                  <Input placeholder="+1 (555) 123-4567" />
                </FormControl>
              </VStack>
            </VStack>
          </Box>

          {/* Notification Settings */}
          <Box
            bg={bgColor}
            p={6}
            borderRadius="lg"
            border="1px"
            borderColor={borderColor}
          >
            <VStack spacing={6} align="start">
              <HStack>
                <Icon as={FiBell} />
                <Heading size="md">Notification Settings</Heading>
              </HStack>
              <VStack spacing={4} align="start" w="100%">
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
                <FormControl>
                  <FormLabel>Notification Frequency</FormLabel>
                  <Select defaultValue="daily">
                    <option value="realtime">Real-time</option>
                    <option value="daily">Daily Digest</option>
                    <option value="weekly">Weekly Summary</option>
                  </Select>
                </FormControl>
              </VStack>
            </VStack>
          </Box>

          {/* Security Settings */}
          <Box
            bg={bgColor}
            p={6}
            borderRadius="lg"
            border="1px"
            borderColor={borderColor}
          >
            <VStack spacing={6} align="start">
              <HStack>
                <Icon as={FiLock} />
                <Heading size="md">Security Settings</Heading>
              </HStack>
              <VStack spacing={4} align="start" w="100%">
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
            </VStack>
          </Box>

          {/* Preferences */}
          <Box
            bg={bgColor}
            p={6}
            borderRadius="lg"
            border="1px"
            borderColor={borderColor}
          >
            <VStack spacing={6} align="start">
              <HStack>
                <Icon as={FiUser} />
                <Heading size="md">Preferences</Heading>
              </HStack>
              <VStack spacing={4} align="start" w="100%">
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
            </VStack>
          </Box>
        </Grid>

        <HStack justify="flex-end">
          <Button variant="outline">Cancel</Button>
          <Button leftIcon={<FiSave />} colorScheme="primary">
            Save Changes
          </Button>
        </HStack>
      </VStack>
    </Box>
  );
};

export default Settings; 