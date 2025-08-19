from user import User

class Rider(User):
    def __init__(self, name:str, contact:str):
        super().__init__(name, contact)
