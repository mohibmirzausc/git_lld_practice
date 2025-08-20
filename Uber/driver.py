from user import User
from driverstatus import DriverStatus

class Driver(User):
    def __init__(self, name:str, contact:str, location:'Location'):
        super().__init__(name, contact)
        self.location = location
        self.status = DriverStatus.AVAILABLE

    def get_location(self) -> 'Location':
        return self.location
    
    def get_state(self) -> DriverStatus:
        return self.status

    def set_status(self, status: DriverStatus):
        self.status = status
