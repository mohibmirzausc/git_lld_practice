from datetime import datetime

class Message:
    def __init__(self, text: str) -> None:
        self.text = text
        self.timestamp = datetime.now()

    def get_text(self):
        return self.text
    
    def get_timestamp(self) -> datetime:
        return self.timestamp
    
    def __str__(self) -> str:
        return self.text