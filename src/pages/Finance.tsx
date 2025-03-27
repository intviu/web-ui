import React from 'react';
import {
  Box,
  Grid,
  Heading,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
  HStack,
  Badge,
  useColorModeValue,
} from '@chakra-ui/react';
import { FiPlus, FiDownload } from 'react-icons/fi';

const Finance = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const transactions = [
    {
      id: 1,
      date: '2024-03-25',
      description: 'Client Payment - Tech Solutions Inc.',
      amount: 5000,
      type: 'Income',
      status: 'Completed',
    },
    {
      id: 2,
      date: '2024-03-24',
      description: 'Office Supplies',
      amount: 250,
      type: 'Expense',
      status: 'Completed',
    },
    {
      id: 3,
      date: '2024-03-23',
      description: 'Client Payment - Marketing Pro',
      amount: 3500,
      type: 'Income',
      status: 'Pending',
    },
    {
      id: 4,
      date: '2024-03-22',
      description: 'Software Subscription',
      amount: 150,
      type: 'Expense',
      status: 'Completed',
    },
  ];

  return (
    <Box p={6}>
      <HStack justify="space-between" mb={6}>
        <Heading size="lg">Finance</Heading>
        <HStack>
          <Button leftIcon={<FiDownload />} variant="outline">
            Export
          </Button>
          <Button leftIcon={<FiPlus />} colorScheme="primary">
            Add Transaction
          </Button>
        </HStack>
      </HStack>

      {/* Financial Overview */}
      <Grid templateColumns="repeat(4, 1fr)" gap={6} mb={6}>
        <Box bg={bgColor} p={6} borderRadius="lg" border="1px" borderColor={borderColor}>
          <Stat>
            <StatLabel>Total Revenue</StatLabel>
            <StatNumber>$45,250</StatNumber>
            <StatHelpText>
              <StatArrow type="increase" />
              12.5%
            </StatHelpText>
          </Stat>
        </Box>
        <Box bg={bgColor} p={6} borderRadius="lg" border="1px" borderColor={borderColor}>
          <Stat>
            <StatLabel>Total Expenses</StatLabel>
            <StatNumber>$12,450</StatNumber>
            <StatHelpText>
              <StatArrow type="decrease" />
              5.2%
            </StatHelpText>
          </Stat>
        </Box>
        <Box bg={bgColor} p={6} borderRadius="lg" border="1px" borderColor={borderColor}>
          <Stat>
            <StatLabel>Net Profit</StatLabel>
            <StatNumber>$32,800</StatNumber>
            <StatHelpText>
              <StatArrow type="increase" />
              15.8%
            </StatHelpText>
          </Stat>
        </Box>
        <Box bg={bgColor} p={6} borderRadius="lg" border="1px" borderColor={borderColor}>
          <Stat>
            <StatLabel>Pending Payments</StatLabel>
            <StatNumber>$8,500</StatNumber>
            <StatHelpText>3 invoices</StatHelpText>
          </Stat>
        </Box>
      </Grid>

      {/* Recent Transactions */}
      <Box bg={bgColor} borderRadius="lg" border="1px" borderColor={borderColor}>
        <Box p={4} borderBottom="1px" borderColor={borderColor}>
          <Heading size="md">Recent Transactions</Heading>
        </Box>
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>Date</Th>
              <Th>Description</Th>
              <Th>Amount</Th>
              <Th>Type</Th>
              <Th>Status</Th>
            </Tr>
          </Thead>
          <Tbody>
            {transactions.map((transaction) => (
              <Tr key={transaction.id}>
                <Td>{transaction.date}</Td>
                <Td>{transaction.description}</Td>
                <Td color={transaction.type === 'Income' ? 'green.500' : 'red.500'}>
                  {transaction.type === 'Income' ? '+' : '-'}${transaction.amount}
                </Td>
                <Td>
                  <Badge colorScheme={transaction.type === 'Income' ? 'green' : 'red'}>
                    {transaction.type}
                  </Badge>
                </Td>
                <Td>
                  <Badge colorScheme={transaction.status === 'Completed' ? 'green' : 'yellow'}>
                    {transaction.status}
                  </Badge>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    </Box>
  );
};

export default Finance; 