from typing_extensions import Self
from typing import Dict
from user import User, Driver, Customer
from restaurant import Restaurant
from order import Order


class Service:
    _instance = None

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self) -> None:
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

    def place_order(self, order: Order):
        self.active_orders.add(order)

    

        
            

    

    
