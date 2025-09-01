import threading
import time
import random
import unittest
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter

from pubsubservice import PubSubService
from topic import Topic
from subscriber import Subscriber
from publisher import Publisher
from message import Message


class MultiThreadRaceConditionTests(unittest.TestCase):
    """Tests to detect race conditions in the pub-sub system"""
    
    def setUp(self):
        """Reset singleton state before each test"""
        # Reset singleton state (for testing purposes)
        PubSubService._instance = None
        PubSubService._initialized = False
    
    def test_singleton_creation_race_condition(self):
        """Test that only one singleton instance is created under heavy concurrent access"""
        instances = []
        instances_lock = threading.Lock()
        
        def create_service():
            service = PubSubService()
            with instances_lock:
                instances.append(service)
        
        # Create 50 threads trying to create the singleton simultaneously
        threads = []
        for _ in range(50):
            thread = threading.Thread(target=create_service)
            threads.append(thread)
        
        # Start all threads simultaneously
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All instances should be the same object
        self.assertEqual(len(instances), 50)
        first_instance = instances[0]
        for instance in instances:
            self.assertIs(instance, first_instance, "Multiple singleton instances created!")
        
        # Service should be properly initialized
        self.assertIsInstance(first_instance.topics, dict)
        self.assertIsInstance(first_instance.publishers, dict)
        self.assertIsInstance(first_instance.subscribers, dict)
    
    def test_pubsubservice_register_race_conditions(self):
        """Test concurrent registration of publishers, subscribers, and topics"""
        service = PubSubService()
        
        # Results tracking
        publisher_results = []
        subscriber_results = []
        topic_results = []
        
        result_lock = threading.Lock()
        
        def register_publishers():
            results = []
            for i in range(100):
                result = service.register_publisher(f"publisher_{i}")
                results.append(result)
            with result_lock:
                publisher_results.extend(results)
        
        def register_subscribers():
            results = []
            for i in range(100):
                result = service.register_subscriber(f"subscriber_{i}")
                results.append(result)
            with result_lock:
                subscriber_results.extend(results)
        
        def register_topics():
            results = []
            for i in range(100):
                result = service.register_topic(f"topic_{i}")
                results.append(result)
            with result_lock:
                topic_results.extend(results)
        
        # Run concurrent registrations
        threads = [
            threading.Thread(target=register_publishers),
            threading.Thread(target=register_subscribers),
            threading.Thread(target=register_topics)
        ]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All registrations should succeed exactly once
        self.assertEqual(sum(publisher_results), 100, "Publisher registration race condition detected!")
        self.assertEqual(sum(subscriber_results), 100, "Subscriber registration race condition detected!")
        self.assertEqual(sum(topic_results), 100, "Topic registration race condition detected!")
        
        # Verify all were actually registered
        self.assertEqual(len(service.publishers), 100)
        self.assertEqual(len(service.subscribers), 100)
        self.assertEqual(len(service.topics), 100)
    
    def test_duplicate_registration_race_condition(self):
        """Test race conditions when multiple threads try to register the same name"""
        service = PubSubService()
        
        publisher_results = []
        result_lock = threading.Lock()
        
        def try_register_same_publisher():
            # All threads try to register the same publisher
            result = service.register_publisher("duplicate_publisher")
            with result_lock:
                publisher_results.append(result)
        
        # 20 threads trying to register the same publisher
        threads = []
        for _ in range(20):
            thread = threading.Thread(target=try_register_same_publisher)
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Only one should succeed, rest should return False
        successful_registrations = sum(publisher_results)
        self.assertEqual(successful_registrations, 1, 
                        f"Expected 1 successful registration, got {successful_registrations}")
        
        # Should have exactly one publisher registered
        self.assertEqual(len(service.publishers), 1)
        self.assertIn("duplicate_publisher", service.publishers)
    
    def test_topic_subscriber_race_conditions(self):
        """Test concurrent adding/removing of subscribers to topics"""
        topic = Topic("test_topic")
        
        # Create subscribers
        subscribers = [Subscriber(f"user_{i}") for i in range(50)]
        
        add_results = []
        remove_results = []
        result_lock = threading.Lock()
        
        def add_subscribers():
            results = []
            for subscriber in subscribers:
                result = topic.add_subscriber(subscriber)
                results.append(result)
            with result_lock:
                add_results.extend(results)
        
        def remove_subscribers():
            # Wait a bit to let some adds happen first
            time.sleep(0.01)
            results = []
            for subscriber in subscribers[:25]:  # Remove half
                result = topic.remove_subscriber(subscriber)
                results.append(result)
            with result_lock:
                remove_results.extend(results)
        
        # Run concurrent add/remove operations
        add_thread = threading.Thread(target=add_subscribers)
        remove_thread = threading.Thread(target=remove_subscribers)
        
        add_thread.start()
        remove_thread.start()
        
        add_thread.join()
        remove_thread.join()
        
        # All adds should succeed
        self.assertEqual(sum(add_results), 50, "Not all subscriber additions succeeded")
        
        # All removes should succeed (since we waited for adds)
        self.assertEqual(sum(remove_results), 25, "Not all subscriber removals succeeded")
        
        # Should have 25 subscribers left
        self.assertEqual(len(topic.subscribers), 25)
    
    def test_concurrent_message_publishing(self):
        """Test race conditions during message publishing"""
        topic = Topic("news")
        
        # Add subscribers
        subscribers = [Subscriber(f"reader_{i}") for i in range(10)]
        for subscriber in subscribers:
            topic.add_subscriber(subscriber)
        
        messages_sent = []
        messages_lock = threading.Lock()
        
        def publish_messages(thread_id):
            for i in range(50):
                message = f"Message_{thread_id}_{i}"
                topic.publish(message)
                with messages_lock:
                    messages_sent.append(message)
                time.sleep(0.001)  # Small delay to increase chance of race conditions
        
        # 5 threads publishing simultaneously
        threads = []
        for thread_id in range(5):
            thread = threading.Thread(target=publish_messages, args=(thread_id,))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should have sent 250 messages total
        self.assertEqual(len(messages_sent), 250)
        
        # Each subscriber should have received all messages
        for subscriber in subscribers:
            # Note: This test depends on current implementation using lists
            # If you switch to queues, you'll need to modify this
            if hasattr(subscriber, 'messages'):
                self.assertEqual(len(subscriber.messages), 250, 
                               f"Subscriber {subscriber.id} didn't receive all messages")
    
    def test_subscriber_message_race_conditions(self):
        """Test race conditions in subscriber message handling"""
        subscriber = Subscriber("test_user")
        
        messages_to_send = []
        for i in range(1000):
            messages_to_send.append(Message(f"Message_{i}"))
        
        def send_messages(start_idx, end_idx):
            for i in range(start_idx, end_idx):
                subscriber.receive_message(messages_to_send[i])
        
        # Split messages among 10 threads
        threads = []
        chunk_size = 100
        for i in range(10):
            start = i * chunk_size
            end = start + chunk_size
            thread = threading.Thread(target=send_messages, args=(start, end))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should have received all 1000 messages
        if hasattr(subscriber, 'messages'):
            self.assertEqual(len(subscriber.messages), 1000, 
                           "Message loss detected in subscriber!")
        elif hasattr(subscriber, 'message_queue'):
            # If using queue implementation
            message_count = subscriber.message_queue.qsize()
            self.assertEqual(message_count, 1000, 
                           "Message loss detected in subscriber queue!")
    
    def test_publisher_topic_management_race_conditions(self):
        """Test race conditions in publisher topic management"""
        publisher = Publisher("news_publisher")
        
        # Create topics
        topics = [Topic(f"topic_{i}") for i in range(50)]
        
        add_results = []
        remove_results = []
        result_lock = threading.Lock()
        
        def add_topics():
            results = []
            for topic in topics:
                result = publisher.add_topic(topic)
                results.append(result)
            with result_lock:
                add_results.extend(results)
        
        def remove_topics():
            time.sleep(0.01)  # Let some adds happen first
            results = []
            for topic in topics[:25]:  # Remove half
                result = publisher.remove_topic(topic)
                results.append(result)
            with result_lock:
                remove_results.extend(results)
        
        add_thread = threading.Thread(target=add_topics)
        remove_thread = threading.Thread(target=remove_topics)
        
        add_thread.start()
        remove_thread.start()
        
        add_thread.join()
        remove_thread.join()
        
        # All adds should succeed
        self.assertEqual(sum(add_results), 50, "Not all topic additions succeeded")
        
        # All removes should succeed
        self.assertEqual(sum(remove_results), 25, "Not all topic removals succeeded")
        
        # Should have 25 topics left
        self.assertEqual(len(publisher.topics), 25)
    
    def test_stress_full_system_race_conditions(self):
        """Stress test the entire system with mixed operations"""
        service = PubSubService()
        
        # Pre-register some entities
        for i in range(10):
            service.register_topic(f"topic_{i}")
            service.register_publisher(f"publisher_{i}")
            service.register_subscriber(f"subscriber_{i}")
        
        operations_completed = []
        operations_lock = threading.Lock()
        
        def mixed_operations(thread_id):
            ops_count = 0
            for i in range(100):
                # Random operations
                operation = random.choice(['subscribe', 'publish', 'register'])
                
                if operation == 'subscribe':
                    topic_name = f"topic_{random.randint(0, 9)}"
                    subscriber_name = f"subscriber_{random.randint(0, 9)}"
                    service.subscribe(subscriber_name, topic_name)
                    ops_count += 1
                
                elif operation == 'publish':
                    topic_name = f"topic_{random.randint(0, 9)}"
                    if topic_name in service.topics:
                        service.topics[topic_name].publish(f"Message from thread {thread_id}")
                    ops_count += 1
                
                elif operation == 'register':
                    # Try to register new entities (most will fail due to duplicates)
                    service.register_topic(f"new_topic_{thread_id}_{i}")
                    service.register_publisher(f"new_publisher_{thread_id}_{i}")
                    service.register_subscriber(f"new_subscriber_{thread_id}_{i}")
                    ops_count += 3
                
                time.sleep(0.001)  # Small delay
            
            with operations_lock:
                operations_completed.append(ops_count)
        
        # Run 10 threads with mixed operations
        threads = []
        for thread_id in range(10):
            thread = threading.Thread(target=mixed_operations, args=(thread_id,))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # System should still be in a consistent state
        self.assertGreater(len(service.topics), 10)  # Should have at least original + some new ones
        self.assertGreater(len(service.publishers), 10)
        self.assertGreater(len(service.subscribers), 10)
        
        # All operations should have completed without crashes
        total_operations = sum(operations_completed)
        self.assertGreater(total_operations, 1000)  # Should have completed many operations


class ThreadSafetyValidationTests(unittest.TestCase):
    """Tests to validate that fixes actually work"""
    
    def setUp(self):
        PubSubService._instance = None
        PubSubService._initialized = False
    
    def test_no_duplicate_singleton_instances(self):
        """Validate that singleton fix prevents duplicate instances"""
        def get_instance():
            return PubSubService()
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(get_instance) for _ in range(100)]
            instances = [future.result() for future in as_completed(futures)]
        
        # All should be the same instance
        first_instance = instances[0]
        for instance in instances:
            self.assertIs(instance, first_instance)
    
    def test_no_lost_registrations(self):
        """Validate that registration fixes prevent lost registrations"""
        service = PubSubService()
        
        def register_items(start, end):
            results = []
            for i in range(start, end):
                results.append(service.register_publisher(f"pub_{i}"))
                results.append(service.register_subscriber(f"sub_{i}"))
                results.append(service.register_topic(f"topic_{i}"))
            return results
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for i in range(10):
                start = i * 100
                end = start + 100
                futures.append(executor.submit(register_items, start, end))
            
            all_results = []
            for future in as_completed(futures):
                all_results.extend(future.result())
        
        # All registrations should succeed
        successful_registrations = sum(all_results)
        self.assertEqual(successful_registrations, 3000)  # 10 threads * 100 items * 3 types
        
        # Verify actual counts
        self.assertEqual(len(service.publishers), 1000)
        self.assertEqual(len(service.subscribers), 1000)
        self.assertEqual(len(service.topics), 1000)


if __name__ == '__main__':
    print("🧵 Running Multithreading Race Condition Tests...")
    print("⚠️  These tests are designed to detect race conditions.")
    print("⚠️  If your code has race conditions, these tests may fail intermittently.")
    print("⚠️  Run multiple times to increase chance of catching race conditions.\n")
    
    unittest.main(verbosity=2) 