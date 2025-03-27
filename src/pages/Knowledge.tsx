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
  useColorModeValue,
  Icon,
  Badge,
} from '@chakra-ui/react';
import { FiSearch, FiBook, FiFileText, FiVideo, FiHelpCircle } from 'react-icons/fi';

const Knowledge = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const articles = [
    {
      id: 1,
      title: 'Getting Started with Business Automation',
      category: 'Automation',
      type: 'article',
      description: 'Learn the basics of automating your business processes and workflows.',
      readTime: '5 min read',
      lastUpdated: '2 days ago',
    },
    {
      id: 2,
      title: 'Video: Customer Service Best Practices',
      category: 'Customer Service',
      type: 'video',
      description: 'Watch this video to learn how to provide exceptional customer service.',
      readTime: '15 min',
      lastUpdated: '1 week ago',
    },
    {
      id: 3,
      title: 'Financial Management Guide',
      category: 'Finance',
      type: 'article',
      description: 'Comprehensive guide to managing your business finances effectively.',
      readTime: '8 min read',
      lastUpdated: '3 days ago',
    },
  ];

  const categories = [
    { name: 'All', count: 45 },
    { name: 'Automation', count: 12 },
    { name: 'Customer Service', count: 8 },
    { name: 'Finance', count: 15 },
    { name: 'Marketing', count: 10 },
  ];

  return (
    <Box p={6}>
      <VStack spacing={6} align="stretch">
        <HStack justify="space-between">
          <Heading size="lg">Knowledge Base</Heading>
          <Button leftIcon={<FiHelpCircle />} colorScheme="primary">
            Ask for Help
          </Button>
        </HStack>

        <InputGroup>
          <InputLeftElement pointerEvents="none">
            <Icon as={FiSearch} color="gray.400" />
          </InputLeftElement>
          <Input placeholder="Search articles, guides, and videos..." />
        </InputGroup>

        <Grid templateColumns="250px 1fr" gap={6}>
          <Box>
            <VStack align="start" spacing={4}>
              <Text fontWeight="bold" mb={2}>Categories</Text>
              {categories.map((category) => (
                <Button
                  key={category.name}
                  variant="ghost"
                  justifyContent="space-between"
                  w="100%"
                  size="sm"
                >
                  <HStack>
                    <Text>{category.name}</Text>
                    <Badge colorScheme="gray">{category.count}</Badge>
                  </HStack>
                </Button>
              ))}
            </VStack>
          </Box>

          <VStack spacing={6} align="stretch">
            {articles.map((article) => (
              <Box
                key={article.id}
                bg={bgColor}
                p={6}
                borderRadius="lg"
                border="1px"
                borderColor={borderColor}
              >
                <VStack align="start" spacing={4}>
                  <HStack justify="space-between" w="100%">
                    <HStack>
                      <Icon
                        as={article.type === 'video' ? FiVideo : FiFileText}
                        color="primary.500"
                      />
                      <Text fontWeight="bold">{article.title}</Text>
                    </HStack>
                    <Badge colorScheme="blue">{article.category}</Badge>
                  </HStack>
                  <Text color="gray.600">{article.description}</Text>
                  <HStack spacing={4}>
                    <Text fontSize="sm" color="gray.500">
                      {article.readTime}
                    </Text>
                    <Text fontSize="sm" color="gray.500">
                      Updated {article.lastUpdated}
                    </Text>
                  </HStack>
                </VStack>
              </Box>
            ))}
          </VStack>
        </Grid>
      </VStack>
    </Box>
  );
};

export default Knowledge; 