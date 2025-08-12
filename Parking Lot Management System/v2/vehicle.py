from abc import ABC

class Vehicle(ABC):
    def __init__(self, license_plate, size):
        self.license_plate = license_plate
        self.size = size
        
    def getSize(self):
        return self.size
    
    def getLicensePlate(self):
        return self.license_plate
    
    
class Car(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, 2)

class Bike(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, 1)

class Truck(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, 3)

