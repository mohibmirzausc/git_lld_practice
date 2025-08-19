from user import User

class Driver(User):
    def __init__(self, name:str, contact:str, location:'Location'):
        super().__init__(name, contact)
        self.location = location

    def get_location(self) -> 'Location':
        return self.location
