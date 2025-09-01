from topic import Topic
from threading import Lock

class Publisher:
    def __init__(self, name: str) -> None:
        self.name = name
        self.topics: list[Topic] = []  # Initialize as empty list
        self._lock = Lock()

    def publish(self, topic: Topic, message: str) -> bool:
        with self._lock:
            if not topic in self.topics:
                print(f"[WARNING] Publisher {self.name} tried to publish to topic {topic.get_name()} that it isn't a publisher of.")
                return False
            
            topic.publish(message)
            return True

    def mass_publish(self, message: str):
        with self._lock:
            for topic in self.topics:
                topic.publish(message)

    def add_topic(self, topic: Topic) -> bool:
        with self._lock:
            if topic in self.topics:
                print(f"[WARNING]: Publisher {self.name} tried to add topic {topic.name} but it's already added")
                return False
            self.topics.append(topic)
            return True
    
    def remove_topic(self, topic: Topic) -> bool:
        with self._lock:
            if not topic in self.topics:
                print(f"[WARNING]: Publisher {self.name} tried to remove topic {topic.name} but it's not a publisher of that topic.")
                return False
            self.topics.remove(topic)
            return True
   