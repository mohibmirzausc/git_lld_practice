from user import User

class Expense:
    def __init__(self, cost: int, name: str, payer: User) -> None:
        self.cost = cost
        self.name = name
        self.payer = payer

    def get_name(self) -> str:
        return self.name
    
    def get_cost(self) -> int:
        return self.cost
    
    def get_payer(self) -> User:
        return self.payer
    
    class ExpenseBuilder:
        
            


