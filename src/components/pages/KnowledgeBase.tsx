import React from 'react';
import {
  Box,
  Grid,
  Heading,
  Text,
  VStack,
  HStack,
  Button,
  Input,
  InputGroup,
  InputLeftElement,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Badge,
  useColorModeValue,
  Icon,
} from '@chakra-ui/react';
import { FiSearch, FiBook, FiPlus, FiTag, FiClock, FiUser } from 'react-icons/fi';

const KnowledgeBase = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const categories = [
    { id: 1, name: 'Getting Started', count: 12 },
    { id: 2, name: 'Client Management', count: 8 },
    { id: 3, name: 'Finance & Billing', count: 15 },
    { id: 4, name: 'Project Management', count: 10 },
    { id: 5, name: 'Social Media', count: 6 },
    { id: 6, name: 'Automation', count: 9 },
  ];

  const articles = [
    {
      id: 1,
      title: 'How to Set Up Your First Project',
      category: 'Getting Started',
      author: 'John Smith',
      date: '2024-03-20',
      readTime: '5 min read',
      tags: ['Setup', 'Projects', 'Guide'],
    },
    {
      id: 2,
      title: 'Managing Client Expectations',
      category: 'Client Management',
      author: 'Sarah Johnson',
      date: '2024-03-19',
      readTime: '8 min read',
      tags: ['Clients', 'Communication', 'Best Practices'],
    },
    {
      id: 3,
      title: 'Automating Invoice Generation',
      category: 'Finance & Billing',
      author: 'Michael Brown',
      date: '2024-03-18',
      readTime: '6 min read',
      tags: ['Finance', 'Automation', 'Invoices'],
    },
  ];

  return (
    <Box p={6}>
      <VStack spacing={6} align="stretch">
        <HStack justify="space-between">
          <Heading size="lg">Knowledge Base</Heading>
          <Button leftIcon={<FiPlus />} colorScheme="primary">
            New Article
          </Button>
        </HStack>

        <InputGroup maxW="400px">
          <InputLeftElement pointerEvents="none">
            <Icon as={FiSearch} color="gray.300" />
          </InputLeftElement>
          <Input placeholder="Search articles..." />
        </InputGroup>

        <Grid templateColumns="repeat(3, 1fr)" gap={6}>
          {/* Categories */}
          <VStack align="start" spacing={4}>
            <Heading size="md">Categories</Heading>
            {categories.map((category) => (
              <Card key={category.id} w="100%" variant="outline">
                <CardBody>
                  <HStack justify="space-between">
                    <HStack>
                      <Icon as={FiBook} />
                      <Text>{category.name}</Text>
                    </HStack>
                    <Badge colorScheme="blue">{category.count}</Badge>
                  </HStack>
                </CardBody>
              </Card>
            ))}
          </VStack>

          {/* Articles */}
          <Grid templateColumns="repeat(2, 1fr)" gap={4} gridColumn="span 2">
            {articles.map((article) => (
              <Card key={article.id} variant="outline">
                <CardHeader>
                  <VStack align="start" spacing={2}>
                    <Heading size="md">{article.title}</Heading>
                    <HStack spacing={4}>
                      <HStack>
                        <Icon as={FiUser} />
                        <Text fontSize="sm">{article.author}</Text>
                      </HStack>
                      <HStack>
                        <Icon as={FiClock} />
                        <Text fontSize="sm">{article.readTime}</Text>
                      </HStack>
                    </HStack>
                  </VStack>
                </CardHeader>
                <CardBody>
                  <VStack align="start" spacing={2}>
                    <HStack>
                      <Icon as={FiTag} />
                      <Text fontSize="sm" color="gray.600">{article.category}</Text>
                    </HStack>
                    <HStack spacing={2}>
                      {article.tags.map((tag) => (
                        <Badge key={tag} colorScheme="gray">{tag}</Badge>
                      ))}
                    </HStack>
                  </VStack>
                </CardBody>
                <CardFooter>
                  <Button variant="ghost" colorScheme="primary">
                    Read More
                  </Button>
                </CardFooter>
              </Card>
            ))}
          </Grid>
        </Grid>
      </VStack>
    </Box>
  );
};

export default KnowledgeBase; 