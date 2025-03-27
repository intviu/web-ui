import React from 'react';
import {
  Box,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
  HStack,
  Badge,
  Avatar,
  Text,
  useColorModeValue,
} from '@chakra-ui/react';
import { FiPlus, FiEdit2, FiTrash2 } from 'react-icons/fi';

const Clients = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const clients = [
    {
      id: 1,
      name: 'John Smith',
      company: 'Tech Solutions Inc.',
      email: 'john@techsolutions.com',
      status: 'Active',
      projects: 3,
      lastContact: '2024-03-20',
    },
    {
      id: 2,
      name: 'Sarah Johnson',
      company: 'Marketing Pro',
      email: 'sarah@marketingpro.com',
      status: 'Active',
      projects: 2,
      lastContact: '2024-03-18',
    },
    {
      id: 3,
      name: 'Michael Brown',
      company: 'Global Industries',
      email: 'michael@globalind.com',
      status: 'Inactive',
      projects: 1,
      lastContact: '2024-02-15',
    },
    {
      id: 4,
      name: 'Emily Davis',
      company: 'Creative Studios',
      email: 'emily@creativestudios.com',
      status: 'Active',
      projects: 4,
      lastContact: '2024-03-22',
    },
  ];

  return (
    <Box p={6}>
      <HStack justify="space-between" mb={6}>
        <Heading size="lg">Clients</Heading>
        <Button leftIcon={<FiPlus />} colorScheme="primary">
          Add Client
        </Button>
      </HStack>

      <Box bg={bgColor} borderRadius="lg" border="1px" borderColor={borderColor}>
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>Client</Th>
              <Th>Company</Th>
              <Th>Status</Th>
              <Th>Projects</Th>
              <Th>Last Contact</Th>
              <Th>Actions</Th>
            </Tr>
          </Thead>
          <Tbody>
            {clients.map((client) => (
              <Tr key={client.id}>
                <Td>
                  <HStack>
                    <Avatar size="sm" name={client.name} />
                    <Box>
                      <Text fontWeight="medium">{client.name}</Text>
                      <Text fontSize="sm" color="gray.600">{client.email}</Text>
                    </Box>
                  </HStack>
                </Td>
                <Td>{client.company}</Td>
                <Td>
                  <Badge
                    colorScheme={client.status === 'Active' ? 'green' : 'gray'}
                  >
                    {client.status}
                  </Badge>
                </Td>
                <Td>{client.projects}</Td>
                <Td>{client.lastContact}</Td>
                <Td>
                  <HStack spacing={2}>
                    <Button size="sm" variant="ghost" leftIcon={<FiEdit2 />}>
                      Edit
                    </Button>
                    <Button size="sm" variant="ghost" colorScheme="red" leftIcon={<FiTrash2 />}>
                      Delete
                    </Button>
                  </HStack>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </Box>
    </Box>
  );
};

export default Clients; 