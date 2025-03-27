import React from 'react';
import {
  Box,
  Grid,
  Heading,
  Text,
  VStack,
  HStack,
  Button,
  Avatar,
  Badge,
  useColorModeValue,
  Icon,
} from '@chakra-ui/react';
import { FiPlus, FiShare2, FiHeart, FiMessageCircle, FiBarChart2 } from 'react-icons/fi';

const Social = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  const posts = [
    {
      id: 1,
      platform: 'LinkedIn',
      content: 'Excited to announce our new partnership with Tech Solutions Inc! 🚀',
      author: 'John Smith',
      likes: 45,
      comments: 12,
      shares: 8,
      timestamp: '2 hours ago',
    },
    {
      id: 2,
      platform: 'Twitter',
      content: 'Check out our latest blog post on digital transformation! #DigitalTransformation #Tech',
      author: 'Sarah Johnson',
      likes: 89,
      comments: 23,
      shares: 15,
      timestamp: '4 hours ago',
    },
    {
      id: 3,
      platform: 'Facebook',
      content: 'Join us for our upcoming webinar on business automation!',
      author: 'Michael Brown',
      likes: 67,
      comments: 18,
      shares: 11,
      timestamp: '6 hours ago',
    },
  ];

  const analytics = [
    {
      platform: 'LinkedIn',
      followers: 1250,
      engagement: '4.2%',
      posts: 45,
      growth: '+12%',
    },
    {
      platform: 'Twitter',
      followers: 890,
      engagement: '3.8%',
      posts: 38,
      growth: '+8%',
    },
    {
      platform: 'Facebook',
      followers: 2100,
      engagement: '2.9%',
      posts: 52,
      growth: '+5%',
    },
  ];

  return (
    <Box p={6}>
      <HStack justify="space-between" mb={6}>
        <Heading size="lg">Social Media</Heading>
        <Button leftIcon={<FiPlus />} colorScheme="primary">
          New Post
        </Button>
      </HStack>

      <Grid templateColumns="repeat(3, 1fr)" gap={6} mb={6}>
        {analytics.map((stat) => (
          <Box
            key={stat.platform}
            bg={bgColor}
            p={6}
            borderRadius="lg"
            border="1px"
            borderColor={borderColor}
          >
            <VStack align="start" spacing={2}>
              <HStack>
                <Icon as={FiBarChart2} />
                <Text fontWeight="bold">{stat.platform}</Text>
              </HStack>
              <Text fontSize="2xl" fontWeight="bold">
                {stat.followers}
              </Text>
              <Text color="gray.600">Followers</Text>
              <HStack spacing={4}>
                <Box>
                  <Text fontSize="sm" color="gray.600">Engagement</Text>
                  <Text fontWeight="medium">{stat.engagement}</Text>
                </Box>
                <Box>
                  <Text fontSize="sm" color="gray.600">Posts</Text>
                  <Text fontWeight="medium">{stat.posts}</Text>
                </Box>
                <Box>
                  <Text fontSize="sm" color="gray.600">Growth</Text>
                  <Text fontWeight="medium" color="green.500">{stat.growth}</Text>
                </Box>
              </HStack>
            </VStack>
          </Box>
        ))}
      </Grid>

      <VStack spacing={6} align="stretch">
        {posts.map((post) => (
          <Box
            key={post.id}
            bg={bgColor}
            p={6}
            borderRadius="lg"
            border="1px"
            borderColor={borderColor}
          >
            <VStack align="start" spacing={4}>
              <HStack justify="space-between" w="100%">
                <HStack>
                  <Avatar size="sm" name={post.author} />
                  <Box>
                    <Text fontWeight="bold">{post.author}</Text>
                    <Text fontSize="sm" color="gray.600">{post.timestamp}</Text>
                  </Box>
                </HStack>
                <Badge colorScheme="blue">{post.platform}</Badge>
              </HStack>
              <Text>{post.content}</Text>
              <HStack spacing={4}>
                <Button size="sm" variant="ghost" leftIcon={<FiHeart />}>
                  {post.likes}
                </Button>
                <Button size="sm" variant="ghost" leftIcon={<FiMessageCircle />}>
                  {post.comments}
                </Button>
                <Button size="sm" variant="ghost" leftIcon={<FiShare2 />}>
                  {post.shares}
                </Button>
              </HStack>
            </VStack>
          </Box>
        ))}
      </VStack>
    </Box>
  );
};

export default Social; 