from typing_extensions import Self
from threading import Lock
from trip import Trip

from queue import Queue
class RideShareService:
    _instance = None
    _lock = Lock()

    def __new__(cls) -> Self:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)

        
        
    def __init__(self) -> None:
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self.rides: Queue[Trip] = Queue()
            self.available_drivers = []

    def start(self):
        
        pass

    def request_ride(self, trip: Trip):
        self.rides.put(trip)

    def add_driver(self, driver: Driver):
        pass



    
        
