from threading import Lock
from topic import Topic
from subscriber import Subscriber
from publisher import Publisher

class PubSubService:
    _instance = None
    _initialized = False
    _lock = Lock()
    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        
        return cls._instance
    
    def __init__(self) -> None:
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._initialized = True
                    self.topics: dict[str, Topic] = {}
                    self.publishers: dict[str, Publisher] = {}
                    self.subscribers: dict[str, Subscriber] = {}

    def register_publisher(self, publisher_name: str) -> bool:
        with self._lock:
            if publisher_name in self.publishers:
                return False
            
            self.publishers[publisher_name] = Publisher(publisher_name)

            return True
    
    def register_subscriber(self, subscriber_name: str) -> bool:
        with self._lock:
            if subscriber_name in self.subscribers:
                return False
            
            self.subscribers[subscriber_name] = Subscriber(subscriber_name)

            return True
    

    def register_topic(self, topic_name: str):
        with self._lock:
            if topic_name in self.topics:
                return False
            
            self.topics[topic_name] = Topic(topic_name)
            return True
        
    def register_topic_publisher(self, topic_name: str, publisher_name: str) -> bool:
        with self._lock:
            if not topic_name in self.topics or not publisher_name in self.publishers:
                return False
            
            return self.publishers[publisher_name].add_topic(self.topics[topic_name])
        
    def subscribe(self, subscriber_name: str, topic_name: str) -> bool:
        with self._lock:
            if not subscriber_name in self.subscribers or not topic_name in self.topics:
                return False
            
            return self.topics[topic_name].add_subscriber(self.subscribers[subscriber_name])
        
    def publish(self, publisher_name: str, topic_name: str, message: str) -> bool:
        with self._lock:
            if not topic_name in self.topics or not publisher_name in self.publishers:
                return False
        
            return self.publishers[publisher_name].publish(self.topics[topic_name], message)
        
    def mass_publish(self, publisher_name: str, message: str):
        with self._lock:
            if not publisher_name in self.publishers:
                return False
            
            return self.publishers[publisher_name].mass_publish(message)




    
    



