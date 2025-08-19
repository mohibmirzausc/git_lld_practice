class User:
    def __init__(self, name:str, contact:str):
        self.name = name
        self.contact = contact

    def get_name(self) -> str:
        return self.name
    
    def get_contact(self) -> str:
        return self.contact
        