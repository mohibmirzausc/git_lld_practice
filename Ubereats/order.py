from user import User, Driver, Customer
from restaurant import Restaurant
from typing import Dict
import copy
from enums import OrderStatus

class Order:
    def __init__(self, order_builder: 'OrderBuilder') -> None:
        self.customer = order_builder.customer
        self.restaurant = order_builder.restaurant
        self.items_ordered: Dict[str, int] = copy.deepcopy(order_builder.items_ordered)
        self.price = order_builder.price
        self.order_status = OrderStatus.ACCEPTED
        self.driver = None

    def set_driver(self, driver: Driver):
        self.driver = driver
        # TO DO: Driver's status needs to be set either here or at higher level

    def progress_status(self):
        if self.order_status == OrderStatus.ACCEPTED:
            self.order_status = OrderStatus.PREPARING
        elif self.order_status == OrderStatus.PREPARING:
            self.order_status = OrderStatus.READY
        elif self.order_status == OrderStatus.READY:
            self.order_status = OrderStatus.PICKED_UP



class OrderBuilder:
    def __init__(self) -> None:
        self.customer: Customer = None
        self.restaurant: Restaurant = None
        self.items_ordered: Dict[str, int] = {} # item_name -> amount_ordered 
        self.price = 0

    def set_customer(self, customer: Customer):
        self.customer = customer
        return self

    def set_restaurant(self, restaurant: Restaurant):
        self.restaurant = restaurant
        return self

    def order_item(self, name: str, amount: int):
        if not self.restaurant:
            raise ValueError("Cannot order if restaurant isn't set!")
        
        if not name in self.restaurant.get_items():
            raise ValueError(f"Ordered invalid item {name} from {self.restaurant.name}!")
        
        self.price += self.restaurant.get_item_price(name) * amount

        self.items_ordered[name] = amount
        return self

    def build(self):
        if not self.customer or not self.restaurant or not self.items_ordered:
            raise ValueError("Order build incomplete!")
        
        return Order(self)



    
    

    
