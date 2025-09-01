from typing import Dict
from user import User, Driver, Customer
from restaurant import Restaurant
from order import Order


class Service:
    _instance = None
    _initialized = False

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            self._initialized = True
            self.drivers: Dict[str, Driver] = {}
            self.customers: Dict[str, Customer] = {}
            self.restaurants: Dict[str, Restaurant] = {}
            self.active_orders = set()
            self.orders = {}
    
    def add_user(self, user: User):
        if isinstance(user, Driver):
            self.drivers[user.get_id()] = user
        
        if isinstance(user, Customer):
            self.customers[user.get_id()] = user

    def place_order(self, order: Order, payment_method: PaymentMethod) -> bool:
        pass
    

        
            

    

    
