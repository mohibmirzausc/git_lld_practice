import datetime

class Message:
    def __init__(self, payload: str) -> None:
        self.timestamp = datetime.now()
        self.payload = payload

    def get_payload(self) -> str:
        return self.payload
    
    def __str__(self) -> str:
        print(f"Message{{payload='{self.payload}'}}")