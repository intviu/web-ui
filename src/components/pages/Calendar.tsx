import React from 'react';
import {
  Box,
  Grid,
  Heading,
  Text,
  VStack,
  HStack,
  IconButton,
  Button,
  useColorModeValue,
} from '@chakra-ui/react';
import { FiChevronLeft, FiChevronRight, FiPlus } from 'react-icons/fi';

const Calendar = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const sampleEvents = [
    { date: 15, title: 'Client Meeting', time: '10:00 AM' },
    { date: 20, title: 'Project Deadline', time: '3:00 PM' },
    { date: 25, title: 'Team Sync', time: '2:00 PM' },
  ];

  return (
    <Box p={6}>
      <HStack justify="space-between" mb={6}>
        <Heading size="lg">Calendar</Heading>
        <Button leftIcon={<FiPlus />} colorScheme="primary">
          Add Event
        </Button>
      </HStack>

      <Box bg={bgColor} borderRadius="lg" border="1px" borderColor={borderColor} p={4}>
        {/* Calendar Header */}
        <HStack justify="space-between" mb={4}>
          <HStack>
            <IconButton
              aria-label="Previous month"
              icon={<FiChevronLeft />}
              variant="ghost"
            />
            <Text fontSize="xl" fontWeight="bold">March 2024</Text>
            <IconButton
              aria-label="Next month"
              icon={<FiChevronRight />}
              variant="ghost"
            />
          </HStack>
        </HStack>

        {/* Calendar Grid */}
        <Grid templateColumns="repeat(7, 1fr)" gap={1}>
          {/* Day headers */}
          {days.map((day) => (
            <Box key={day} p={2} textAlign="center" fontWeight="bold">
              {day}
            </Box>
          ))}

          {/* Calendar days */}
          {Array.from({ length: 31 }, (_, i) => (
            <Box
              key={i}
              p={2}
              minH="100px"
              border="1px"
              borderColor={borderColor}
              borderRadius="md"
            >
              <Text fontWeight="bold" mb={2}>
                {i + 1}
              </Text>
              {sampleEvents.map((event) => (
                event.date === i + 1 && (
                  <Box
                    key={event.title}
                    bg="primary.100"
                    p={1}
                    borderRadius="sm"
                    mb={1}
                    fontSize="sm"
                  >
                    <Text fontWeight="medium">{event.title}</Text>
                    <Text fontSize="xs" color="gray.600">{event.time}</Text>
                  </Box>
                )
              ))}
            </Box>
          ))}
        </Grid>
      </Box>
    </Box>
  );
};

export default Calendar; 