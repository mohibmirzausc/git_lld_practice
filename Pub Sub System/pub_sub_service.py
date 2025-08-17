import threading
from typing import Dict
from topic import Topic
from subscriber import Subscriber
from message import Message
from concurrent.futures import ThreadPoolExecutor

class PubSubService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False

                return cls._instance
            
    def __init__(self):
        if self._initalized:
            return 
        
        self.topic_registry: Dict[str, Topic] = {}
        # continue...
        


            