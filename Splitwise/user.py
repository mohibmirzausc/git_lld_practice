from typing import Set

class User:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id

    def get_id(self):
        return self.user_id