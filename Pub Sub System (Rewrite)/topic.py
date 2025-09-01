from subscriber import Subscriber
from message import Message
from threading import Lock

class Topic:
    def __init__(self, name: str) -> None:
        self.name = name
        self.subscribers: list[Subscriber] = []
        self._lock = Lock()

    def get_name(self):
        return self.name

    def publish(self, message: str) -> None:
        message_object = Message(message)

        with self._lock:
            for sub in self.subscribers:
                sub.receive_message(message_object)

    def add_subscriber(self, subscriber: Subscriber) -> bool:
        with self._lock:
            if subscriber in self.subscribers:
                print(f"[WARNING] {subscriber.id} tried to subscribe to Topic {self.name} but is already subscribed to it!")
                return False
            
            self.subscribers.append(subscriber)
            return True
    
    def remove_subscriber(self, subscriber: Subscriber):
        with self._lock:
            if not subscriber in self.subscribers:
                print(f"[WARNING] {subscriber.id} tried to unsubscribe to Topic {self.name} but is not subscribed to it!")
                return False
            
            self.subscribers.remove(subscriber)
            return True

    def check_subscribed(self, subscriber: Subscriber):
        with self._lock:
            return subscriber in self.subscribers

    
    
