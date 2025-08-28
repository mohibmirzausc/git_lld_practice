from abc import ABC, abstractmethod
from enums import UserType, DriverStatus
from typing import List

class User(ABC):
    def __init__(self, id: str, type: UserType) -> None:
        self.id = id
        self.type = type
        self.messages: List[str] = []

    def get_id(self):
        return self.id
    
    def get_type(self):
        return self.type
    
    def receive_notification(self, msg: str):
        print(f"{self.id} received a notification: ", msg)
        self.messages.append(msg)

class Customer(User):
    def __init__(self, id: str) -> None:
        super().__init__(id, UserType.CUSTOMER)
        self.past_orders: List['Order'] = []


    
class Driver(User):
    def __init__(self, id: str) -> None:
        super().__init__(id, UserType.DRIVER)
        self.driver_status: DriverStatus = DriverStatus.AWAITING_ORDER

    def set_driver_status(self, driver_status: DriverStatus):
        self.driver_status = driver_status

    def get_driver_status(self):
        return self.driver_status
    

