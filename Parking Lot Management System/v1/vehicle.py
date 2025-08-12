from enum import Enum
import uuid
from passtype import PassType

class VehicleType(Enum):
    BIKE = 1
    CAR = 2
    TRUCK = 3

class FuelType(Enum):
    Gasoline = 1
    EV = 2
    Diesel = 3

class Vehicle:
    
    def __init__(self, vehicle_type: VehicleType, fuel_type: FuelType, pass_type: PassType):
        self.vehicle_type = vehicle_type
        self.fuel_type = fuel_type
        self.pass_type = pass_type

        self.license_plate = uuid.uuid4()

    def getFuelType(self):
        return self.fuel_type

    def getVehicleType(self):
        return self.vehicle_type

    def getPassType(self):
        return self.pass_type

    def getLicensePlate(self):
        return self.license_plate
        