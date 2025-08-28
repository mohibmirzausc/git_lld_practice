from typing import Dict
import copy

class Restaurant:
    def __init__(self, builder: 'RestaurantBuilder') -> None:
        self.name = builder.name
        self.menu = copy.deepcopy(builder.menu)
    
    def get_name(self):
        return self.name
    
    def get_items(self):
        return self.menu.keys()
    
    def get_item_price(self, item_name: str) -> float:
        item_name = item_name.lower()
        if not self.menu.get(item_name):
            raise ValueError(f"Menu of {self.name} doesn't contain item {item_name}")
        
        return self.menu[item_name]
    
    def __str__(self) -> str:
        s = f"{self.name.capitalize()} offers: \n"
        s += "==============\n"
        for item_name, price in self.menu.items():
            s += f"{item_name}: {price}\n"
        s += "==============\n"

        return s


class RestaurantBuilder:

    def __init__(self) -> None:
        self.name: str = ""
        self.menu: Dict[str, float] = {}

    def set_name(self, name: str):
        self.name = name
        return self
    
    def add_menu_item(self, name: str, price: float):
        self.menu[name.lower()] = round(float(price), 2)
        return self

    def build(self):
        if not self.name or not self.menu:
            raise ValueError("Builder is missing components!")
        return Restaurant(self)
    