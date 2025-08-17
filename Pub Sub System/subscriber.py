from abc import ABC, abstractmethod
from message import Message

class Subscriber(ABC):
    @abstractmethod
    def get_id(self) -> str:
        pass
    
    @abstractmethod
    def on_message(self, message: Message) -> str:
        pass
    
class AlertSubscriber(Subscriber):
    def __init__(self, subscriber_id: str) -> None:
        self.id = subscriber_id

    def get_id(self):
        return self.id
    
    def on_message(self, message: Message) -> None:
        print(f"[ALERT - {self.id}] '{message.get_payload()}'")

class NewsSubscriber(Subscriber):
    def __init__(self, subscriber_id: str) -> None:
        self.id = subscriber_id

    def get_id(self):
        return self.id
    
    def on_message(self, message: Message) -> None:
        print(f"[NEWS - {self.id}] '{message.get_payload()}'")
