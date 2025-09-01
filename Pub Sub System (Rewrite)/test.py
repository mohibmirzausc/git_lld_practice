import unittest
from unittest.mock import patch
from io import StringIO
import sys

from message import Message
from subscriber import Subscriber
from topic import Topic
from publisher import Publisher


class TestMessage(unittest.TestCase):
    """Test cases for Message class"""
    
    def test_message_creation(self):
        """Test that a message can be created with text"""
        text = "Hello, World!"
        message = Message(text)
        self.assertEqual(message.text, text)
    
    def test_get_text(self):
        """Test that get_text returns the correct text"""
        text = "Test message"
        message = Message(text)
        self.assertEqual(message.get_text(), text)
    
    def test_str_representation(self):
        """Test that __str__ returns the message text"""
        text = "String representation test"
        message = Message(text)
        self.assertEqual(str(message), text)
    
    def test_empty_message(self):
        """Test that empty messages can be created"""
        message = Message("")
        self.assertEqual(message.get_text(), "")
        self.assertEqual(str(message), "")


class TestSubscriber(unittest.TestCase):
    """Test cases for Subscriber class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.subscriber = Subscriber("test_user")
    
    def test_subscriber_creation(self):
        """Test that a subscriber can be created with an ID"""
        self.assertEqual(self.subscriber.id, "test_user")
        self.assertEqual(len(self.subscriber.messages), 0)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_receive_message(self, mock_stdout):
        """Test that subscriber can receive messages"""
        message = Message("Test message")
        self.subscriber.receive_message(message)
        
        # Check that message was added to subscriber's messages
        self.assertEqual(len(self.subscriber.messages), 1)
        self.assertEqual(self.subscriber.messages[0], message)
        
        # Check that output was printed
        output = mock_stdout.getvalue()
        self.assertIn("[USER MESSAGE] test_user received a message 'Test message'", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_receive_multiple_messages(self, mock_stdout):
        """Test that subscriber can receive multiple messages"""
        message1 = Message("First message")
        message2 = Message("Second message")
        
        self.subscriber.receive_message(message1)
        self.subscriber.receive_message(message2)
        
        self.assertEqual(len(self.subscriber.messages), 2)
        self.assertEqual(self.subscriber.messages[0], message1)
        self.assertEqual(self.subscriber.messages[1], message2)


class TestTopic(unittest.TestCase):
    """Test cases for Topic class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.topic = Topic("test_topic")
        self.subscriber1 = Subscriber("user1")
        self.subscriber2 = Subscriber("user2")
    
    def test_topic_creation(self):
        """Test that a topic can be created with a name"""
        self.assertEqual(self.topic.name, "test_topic")
        self.assertEqual(len(self.topic.subscribers), 0)
    
    def test_add_subscriber_success(self):
        """Test successfully adding a subscriber to a topic"""
        result = self.topic.add_subscriber(self.subscriber1)
        
        self.assertTrue(result)
        self.assertEqual(len(self.topic.subscribers), 1)
        self.assertIn(self.subscriber1, self.topic.subscribers)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_subscriber_duplicate(self, mock_stdout):
        """Test adding a duplicate subscriber to a topic"""
        # Add subscriber first time
        self.topic.add_subscriber(self.subscriber1)
        
        # Try to add same subscriber again
        result = self.topic.add_subscriber(self.subscriber1)
        
        self.assertFalse(result)
        self.assertEqual(len(self.topic.subscribers), 1)
        
        # Check warning message
        output = mock_stdout.getvalue()
        self.assertIn("[WARNING] user1 tried to subscribe to Topic test_topic but is already subscribed to it!", output)
    
    def test_remove_subscriber_success(self):
        """Test successfully removing a subscriber from a topic"""
        self.topic.add_subscriber(self.subscriber1)
        result = self.topic.remove_subscriber(self.subscriber1)
        
        self.assertTrue(result)
        self.assertEqual(len(self.topic.subscribers), 0)
        self.assertNotIn(self.subscriber1, self.topic.subscribers)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_remove_subscriber_not_subscribed(self, mock_stdout):
        """Test removing a subscriber that is not subscribed"""
        result = self.topic.remove_subscriber(self.subscriber1)
        
        self.assertFalse(result)
        
        # Check warning message
        output = mock_stdout.getvalue()
        self.assertIn("[WARNING] user1 tried to unsubscribe to Topic test_topic but is not subscribed to it!", output)
    
    def test_check_subscribed(self):
        """Test checking if a subscriber is subscribed to a topic"""
        # Initially not subscribed
        self.assertFalse(self.topic.check_subscribed(self.subscriber1))
        
        # After subscribing
        self.topic.add_subscriber(self.subscriber1)
        self.assertTrue(self.topic.check_subscribed(self.subscriber1))
        
        # After unsubscribing
        self.topic.remove_subscriber(self.subscriber1)
        self.assertFalse(self.topic.check_subscribed(self.subscriber1))
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_publish_to_subscribers(self, mock_stdout):
        """Test publishing a message to all subscribers"""
        self.topic.add_subscriber(self.subscriber1)
        self.topic.add_subscriber(self.subscriber2)
        
        message_text = "Hello subscribers!"
        self.topic.publish(message_text)
        
        # Check that both subscribers received the message
        self.assertEqual(len(self.subscriber1.messages), 1)
        self.assertEqual(len(self.subscriber2.messages), 1)
        self.assertEqual(self.subscriber1.messages[0].get_text(), message_text)
        self.assertEqual(self.subscriber2.messages[0].get_text(), message_text)
        
        # Check output
        output = mock_stdout.getvalue()
        self.assertIn("[USER MESSAGE] user1 received a message 'Hello subscribers!'", output)
        self.assertIn("[USER MESSAGE] user2 received a message 'Hello subscribers!'", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_publish_no_subscribers(self, mock_stdout):
        """Test publishing when there are no subscribers"""
        self.topic.publish("No one will receive this")
        
        # Should not crash and no output should be generated
        output = mock_stdout.getvalue()
        self.assertEqual(output, "")


class TestPublisher(unittest.TestCase):
    """Test cases for Publisher class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.publisher = Publisher("test_publisher")
        self.topic1 = Topic("topic1")
        self.topic2 = Topic("topic2")
        self.subscriber = Subscriber("test_subscriber")
    
    def test_publisher_creation(self):
        """Test that a publisher can be created with a name"""
        self.assertEqual(self.publisher.name, "test_publisher")
        self.assertEqual(len(self.publisher.topics), 0)
    
    def test_add_topic_success(self):
        """Test successfully adding a topic to a publisher"""
        result = self.publisher.add_topic(self.topic1)
        
        self.assertTrue(result)
        self.assertEqual(len(self.publisher.topics), 1)
        self.assertIn(self.topic1, self.publisher.topics)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_topic_duplicate(self, mock_stdout):
        """Test adding a duplicate topic to a publisher"""
        # Add topic first time
        self.publisher.add_topic(self.topic1)
        
        # Try to add same topic again
        result = self.publisher.add_topic(self.topic1)
        
        self.assertFalse(result)
        self.assertEqual(len(self.publisher.topics), 1)
        
        # Check warning message
        output = mock_stdout.getvalue()
        self.assertIn("[WARNING]: Publisher test_publisher tried to add topic topic1 but it's already added", output)
    
    def test_remove_topic_success(self):
        """Test successfully removing a topic from a publisher"""
        self.publisher.add_topic(self.topic1)
        result = self.publisher.remove_topic(self.topic1)
        
        self.assertTrue(result)
        self.assertEqual(len(self.publisher.topics), 0)
        self.assertNotIn(self.topic1, self.publisher.topics)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_remove_topic_not_added(self, mock_stdout):
        """Test removing a topic that was not added"""
        result = self.publisher.remove_topic(self.topic1)
        
        self.assertFalse(result)
        
        # Check warning message
        output = mock_stdout.getvalue()
        self.assertIn("[WARNING]: Publisher test_publisher tried to remove topic topic1 but it's not a publisher of that topic.", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_publish_to_specific_topic(self, mock_stdout):
        """Test publishing a message to a specific topic"""
        # Set up topic with subscriber
        self.topic1.add_subscriber(self.subscriber)
        
        message_text = "Specific topic message"
        self.publisher.publish(self.topic1, message_text)
        
        # Subscriber should receive the message
        self.assertEqual(len(self.subscriber.messages), 1)
        self.assertEqual(self.subscriber.messages[0].get_text(), message_text)
        
        # Check output
        output = mock_stdout.getvalue()
        self.assertIn("[USER MESSAGE] test_subscriber received a message 'Specific topic message'", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_mass_publish_to_multiple_topics(self, mock_stdout):
        """Test mass publishing a message to all publisher's topics"""
        # Set up topics with subscribers
        self.topic1.add_subscriber(self.subscriber)
        self.topic2.add_subscriber(self.subscriber)
        
        self.publisher.add_topic(self.topic1)
        self.publisher.add_topic(self.topic2)
        
        message_text = "Mass publish message"
        self.publisher.mass_publish(message_text)
        
        # Subscriber should receive the message twice (once from each topic)
        self.assertEqual(len(self.subscriber.messages), 2)
        self.assertEqual(self.subscriber.messages[0].get_text(), message_text)
        self.assertEqual(self.subscriber.messages[1].get_text(), message_text)
    
    def test_mass_publish_no_topics(self):
        """Test mass publishing when publisher has no topics"""
        # Should not crash
        self.publisher.mass_publish("No topics to publish to")
        # No assertion needed, just making sure it doesn't crash
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_mass_publish_single_topic(self, mock_stdout):
        """Test mass publishing with only one topic"""
        self.topic1.add_subscriber(self.subscriber)
        self.publisher.add_topic(self.topic1)
        
        message_text = "Single topic mass publish"
        self.publisher.mass_publish(message_text)
        
        # Subscriber should receive the message once
        self.assertEqual(len(self.subscriber.messages), 1)
        self.assertEqual(self.subscriber.messages[0].get_text(), message_text)


class TestPubSubIntegration(unittest.TestCase):
    """Integration tests for the entire pub-sub system"""
    
    def setUp(self):
        """Set up a complete pub-sub system for integration testing"""
        self.publisher1 = Publisher("news_publisher")
        self.publisher2 = Publisher("sports_publisher")
        
        self.topic_news = Topic("news")
        self.topic_sports = Topic("sports")
        
        self.subscriber1 = Subscriber("alice")
        self.subscriber2 = Subscriber("bob")
        self.subscriber3 = Subscriber("charlie")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_complete_pubsub_workflow(self, mock_stdout):
        """Test a complete publish-subscribe workflow"""
        # Set up subscriptions
        self.topic_news.add_subscriber(self.subscriber1)
        self.topic_news.add_subscriber(self.subscriber2)
        self.topic_sports.add_subscriber(self.subscriber2)
        self.topic_sports.add_subscriber(self.subscriber3)
        
        # Set up publishers
        self.publisher1.add_topic(self.topic_news)
        self.publisher2.add_topic(self.topic_sports)
        
        # Publish messages
        self.publisher1.publish(self.topic_news, "Breaking news!")
        self.publisher2.publish(self.topic_sports, "Sports update!")
        
        # Verify message delivery
        # Alice should have 1 message (news only)
        self.assertEqual(len(self.subscriber1.messages), 1)
        self.assertEqual(self.subscriber1.messages[0].get_text(), "Breaking news!")
        
        # Bob should have 2 messages (both news and sports)
        self.assertEqual(len(self.subscriber2.messages), 2)
        
        # Charlie should have 1 message (sports only)
        self.assertEqual(len(self.subscriber3.messages), 1)
        self.assertEqual(self.subscriber3.messages[0].get_text(), "Sports update!")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_dynamic_subscription_changes(self, mock_stdout):
        """Test adding and removing subscribers dynamically"""
        self.publisher1.add_topic(self.topic_news)
        
        # Initially no subscribers
        self.publisher1.publish(self.topic_news, "First message")
        self.assertEqual(len(self.subscriber1.messages), 0)
        
        # Add subscriber and publish
        self.topic_news.add_subscriber(self.subscriber1)
        self.publisher1.publish(self.topic_news, "Second message")
        self.assertEqual(len(self.subscriber1.messages), 1)
        
        # Remove subscriber and publish
        self.topic_news.remove_subscriber(self.subscriber1)
        self.publisher1.publish(self.topic_news, "Third message")
        self.assertEqual(len(self.subscriber1.messages), 1)  # Still only 1 message
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_mass_publish_integration(self, mock_stdout):
        """Test mass publish functionality in a complete pub-sub system"""
        # Set up subscriptions
        self.topic_news.add_subscriber(self.subscriber1)
        self.topic_news.add_subscriber(self.subscriber2)
        self.topic_sports.add_subscriber(self.subscriber2)
        self.topic_sports.add_subscriber(self.subscriber3)
        
        # Set up publisher with multiple topics
        self.publisher1.add_topic(self.topic_news)
        self.publisher1.add_topic(self.topic_sports)
        
        # Mass publish to all topics
        self.publisher1.mass_publish("Breaking announcement!")
        
        # Verify message delivery
        # Alice (subscribed to news only) should have 1 message
        self.assertEqual(len(self.subscriber1.messages), 1)
        self.assertEqual(self.subscriber1.messages[0].get_text(), "Breaking announcement!")
        
        # Bob (subscribed to both) should have 2 messages
        self.assertEqual(len(self.subscriber2.messages), 2)
        self.assertEqual(self.subscriber2.messages[0].get_text(), "Breaking announcement!")
        self.assertEqual(self.subscriber2.messages[1].get_text(), "Breaking announcement!")
        
        # Charlie (subscribed to sports only) should have 1 message
        self.assertEqual(len(self.subscriber3.messages), 1)
        self.assertEqual(self.subscriber3.messages[0].get_text(), "Breaking announcement!")
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_publish_vs_mass_publish_comparison(self, mock_stdout):
        """Test the difference between publish and mass_publish methods"""
        # Set up subscriptions
        self.topic_news.add_subscriber(self.subscriber1)
        self.topic_sports.add_subscriber(self.subscriber2)
        
        # Set up publisher with multiple topics
        self.publisher1.add_topic(self.topic_news)
        self.publisher1.add_topic(self.topic_sports)
        
        # Test specific publish - should only go to news topic
        self.publisher1.publish(self.topic_news, "News only message")
        
        # Test mass publish - should go to all topics
        self.publisher1.mass_publish("Mass message")
        
        # Verify results
        # Alice (news subscriber) should have 2 messages
        self.assertEqual(len(self.subscriber1.messages), 2)
        self.assertEqual(self.subscriber1.messages[0].get_text(), "News only message")
        self.assertEqual(self.subscriber1.messages[1].get_text(), "Mass message")
        
        # Bob (sports subscriber) should have 1 message (only the mass publish)
        self.assertEqual(len(self.subscriber2.messages), 1)
        self.assertEqual(self.subscriber2.messages[0].get_text(), "Mass message")


if __name__ == '__main__':
    unittest.main(verbosity=2)
