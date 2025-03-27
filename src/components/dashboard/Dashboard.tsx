import React from 'react';
import {
  Box,
  Grid,
  GridItem,
  Heading,
  Text,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  SimpleGrid,
  Card,
  CardBody,
  Icon,
  Button,
  useColorModeValue,
} from '@chakra-ui/react';
import {
  FiCalendar,
  FiDollarSign,
  FiUsers,
  FiTrendingUp,
  FiMessageSquare,
  FiShare2,
  FiFileText,
} from 'react-icons/fi';

const StatCard: React.FC<{
  label: string;
  value: string;
  change: string;
  icon: React.ElementType;
}> = ({ label, value, change, icon }) => {
  const bgColor = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  return (
    <Card bg={bgColor} borderWidth="1px" borderColor={borderColor}>
      <CardBody>
        <Stat>
          <StatLabel display="flex" alignItems="center">
            <Icon as={icon} mr={2} />
            {label}
          </StatLabel>
          <StatNumber>{value}</StatNumber>
          <StatHelpText>
            <StatArrow type="increase" />
            {change}
          </StatHelpText>
        </Stat>
      </CardBody>
    </Card>
  );
};

const QuickAction: React.FC<{
  icon: React.ElementType;
  label: string;
  onClick: () => void;
}> = ({ icon, label, onClick }) => {
  const bgColor = useColorModeValue('white', 'gray.700');
  const hoverBg = useColorModeValue('gray.50', 'gray.600');

  return (
    <Button
      leftIcon={<Icon as={icon} />}
      variant="ghost"
      justifyContent="flex-start"
      w="full"
      h="auto"
      p={4}
      bg={bgColor}
      _hover={{ bg: hoverBg }}
      onClick={onClick}
    >
      {label}
    </Button>
  );
};

const Dashboard: React.FC = () => {
  const stats = [
    {
      label: 'Today\'s Appointments',
      value: '8',
      change: '2 more than yesterday',
      icon: FiCalendar,
    },
    {
      label: 'Revenue',
      value: '$2,450',
      change: '12% from last week',
      icon: FiDollarSign,
    },
    {
      label: 'New Clients',
      value: '3',
      change: '1 more than last week',
      icon: FiUsers,
    },
    {
      label: 'Growth Rate',
      value: '15%',
      change: '5% from last month',
      icon: FiTrendingUp,
    },
  ];

  const quickActions = [
    { icon: FiCalendar, label: 'Schedule New Appointment' },
    { icon: FiMessageSquare, label: 'Send Client Message' },
    { icon: FiShare2, label: 'Create Social Post' },
    { icon: FiFileText, label: 'Generate Invoice' },
  ];

  return (
    <Box>
      <Heading size="lg" mb={6}>
        Dashboard
      </Heading>

      <Grid templateColumns="repeat(4, 1fr)" gap={6} mb={8}>
        {stats.map((stat) => (
          <GridItem key={stat.label}>
            <StatCard {...stat} />
          </GridItem>
        ))}
      </Grid>

      <Box>
        <Heading size="md" mb={4}>
          Quick Actions
        </Heading>
        <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4}>
          {quickActions.map((action) => (
            <QuickAction
              key={action.label}
              icon={action.icon}
              label={action.label}
              onClick={() => console.log(action.label)}
            />
          ))}
        </SimpleGrid>
      </Box>
    </Box>
  );
};

export default Dashboard; 