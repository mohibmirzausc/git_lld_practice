from abc import ABC, abstractmethod
from typing import Iterable

from vehicle import Vehicle, VehicleType, FuelType
from spot import Spot
from passtype import PassType
from strategy_base import ParkingStrategy

# strategy design pattern
class NoRestriction(ParkingStrategy):
    def can_park(self, spot: Spot, vehicle: Vehicle):
        return True
    
class RequiresSpotType(ParkingStrategy):
    def __init__(self, required: PassType):
        self.required = required

    def can_park(self, spot: Spot, vehicle: Vehicle):
        if vehicle.getPassType().value >= self.required.value:
            return True
        
class RequireVehicleType(ParkingStrategy):
    def __init__(self, vehicles: VehicleType | Iterable[VehicleType]):
        self.vehicle_types = {vehicles} if isinstance(vehicles, VehicleType) else set(vehicles)

    def can_park(self, spot: Spot, vehicle: Vehicle):
        if vehicle.getVehicleType() in self.vehicle_types:
            return True
        
class FuelWhiteList(ParkingStrategy):
    def __init__(self, fuels: FuelType | Iterable[FuelType]):
        self.fuel_types = {fuels} if isinstance(fuels, FuelType) else set(fuels)

    def can_park(self, spot: Spot, vehicle: Vehicle):
        if vehicle.getFuelType() in self.fuel_types:
            return True
        
class And(ParkingStrategy):
    def __init__(self, *rules: ParkingStrategy):
        self.rules = rules

    def can_park(self, spot: Spot, vehicle: Vehicle):
        for rule in self.rules:
            if not rule.can_park(spot, vehicle):
                return False
        return True

class Or(ParkingStrategy):
    def __init__(self, *rules: ParkingStrategy):
        self.rules = rules

    def can_park(self, spot: Spot, vehicle: Vehicle):
        for rule in self.rules:
            if rule.can_park(spot, vehicle):
                return True
            
        return False

        
