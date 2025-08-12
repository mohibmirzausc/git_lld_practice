
from vehicle import Vehicle, VehicleType

from strategy_base import ParkingStrategy

class Spot:

    def __init__(self, vehicle_type: VehicleType, rule: ParkingStrategy): 
        self.vehicle_type = vehicle_type
        self.parked_vehicle = None
        self.parking_start_time = None
        self.rule = rule


    def can_park(self, vehicle: Vehicle):
        if not self.isEmpty():
            return False
        
        return self.rule.can_park(self, vehicle)



    def isEmpty(self):
        return self.parked_vehicle == None
    