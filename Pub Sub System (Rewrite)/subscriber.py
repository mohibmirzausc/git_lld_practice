from message import Message
from threading import Lock

class Subscriber: 
    def __init__(self, id: str) -> None:
        self.id = id
        self.messages: list[Message] = []
        self._lock = Lock()

    def receive_message(self, message: Message):
        with self._lock:
            self.messages.append(message)
            print(f"[USER MESSAGE] {self.id} received a message '{message}'")

    