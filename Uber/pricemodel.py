from typing import Protocol
from trip import Trip
from abc import abstractmethod
from ridetype import RideType

class PriceModel(Protocol):
    def get_cost(self, trip: Trip) -> int:
        pass
    
class EconomyPriceModel(PriceModel):
    def __init__(self, base_price: int, price_per_mile: int, min_price: int) -> None:
        self.base_price = base_price
        self.price_per_mile = price_per_mile
        self.min_price = min_price

    def get_cost(self, trip: Trip) -> int:
        distance = trip.get_distance()

        return max(self.min_price, self.base_price + self.price_per_mile*distance)

class PremiumPriceModel(PriceModel):
    def __init__(self, base_price: int, price_per_mile: int, min_price: int) -> None:
        self.base_price = base_price
        self.price_per_mile = price_per_mile
        self.min_price = min_price

    def get_cost(self, trip: Trip) -> int:
        distance = trip.get_distance()
        # premium pricing may have different logic
        return max(self.min_price, self.base_price + self.price_per_mile*distance)






        