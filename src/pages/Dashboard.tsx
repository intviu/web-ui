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
  CardHeader,
  CardBody,
} from '@chakra-ui/react';

const DashboardCard = ({ title, children }: { title: string; children: React.ReactNode }) => (
  <Card>
    <CardHeader>
      <Heading size="md">{title}</Heading>
    </CardHeader>
    <CardBody>{children}</CardBody>
  </Card>
);

const Dashboard = () => {
  return (
    <Box>
      <Heading mb={6}>Dashboard</Heading>
      
      {/* Key Metrics */}
      <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={4} mb={8}>
        <Stat bg="white" p={4} borderRadius="lg" boxShadow="sm">
          <StatLabel>Revenue</StatLabel>
          <StatNumber>$23,450</StatNumber>
          <StatHelpText>
            <StatArrow type="increase" />
            23.36%
          </StatHelpText>
        </Stat>
        <Stat bg="white" p={4} borderRadius="lg" boxShadow="sm">
          <StatLabel>Active Clients</StatLabel>
          <StatNumber>45</StatNumber>
          <StatHelpText>
            <StatArrow type="increase" />
            9.05%
          </StatHelpText>
        </Stat>
        <Stat bg="white" p={4} borderRadius="lg" boxShadow="sm">
          <StatLabel>Pending Tasks</StatLabel>
          <StatNumber>12</StatNumber>
          <StatHelpText>
            <StatArrow type="decrease" />
            5.25%
          </StatHelpText>
        </Stat>
        <Stat bg="white" p={4} borderRadius="lg" boxShadow="sm">
          <StatLabel>Social Reach</StatLabel>
          <StatNumber>8.9K</StatNumber>
          <StatHelpText>
            <StatArrow type="increase" />
            14.47%
          </StatHelpText>
        </Stat>
      </SimpleGrid>

      {/* Dashboard Grid */}
      <Grid
        templateColumns={{ base: 'repeat(1, 1fr)', lg: 'repeat(3, 1fr)' }}
        gap={6}
      >
        <GridItem colSpan={{ base: 1, lg: 2 }}>
          <DashboardCard title="Recent Activity">
            <Text>Activity timeline will be displayed here</Text>
          </DashboardCard>
        </GridItem>
        
        <GridItem>
          <DashboardCard title="Upcoming Tasks">
            <Text>Task list will be displayed here</Text>
          </DashboardCard>
        </GridItem>

        <GridItem colSpan={{ base: 1, lg: 2 }}>
          <DashboardCard title="Revenue Overview">
            <Text>Revenue chart will be displayed here</Text>
          </DashboardCard>
        </GridItem>

        <GridItem>
          <DashboardCard title="Quick Actions">
            <Text>Action buttons will be displayed here</Text>
          </DashboardCard>
        </GridItem>
      </Grid>
    </Box>
  );
};

export default Dashboard; 