from typing import Set, List
from user import User
from expense import Expense

class Group:
    def __init__(self, id: str, *users: User):
        self.id = id
        self.users: Set[User] = set(users)
        self.expenses: List[Expense] = []

    def add_expense(self, cost: int, name: str, payer: User) -> None:
        if payer in self.users:
            self.expenses.append(Expense(cost,name, payer))

    def __str__(self) -> str:
        user_str = ", ".join(user.get_id() for user in self.users)
        return f"Group {self.id} contains {user_str}."



    

    