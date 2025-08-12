import uuid

class Spot:
    def __init__(self, size):
        self.id = uuid.uuid4()
        self.size = size
        self.is_occupied = False
        self.vehicle = None

    def assign_vehicle(self, vehicle):
        if self.is_occupied:
            print(f"ERROR: Tried to print in a reserved parking spot! (parking id: {self.id}, vehicle lp: {vehicle.getLicensePlate()})")
            return False
        
        if vehicle.getSize() > self.size:
            print(f"ERROR: Tried to park in a smaller parking space! (parking id: {self.id}, vehicle lp: {vehicle.getLicensePlate()})")
            return False
        
        print(f"Parking successful! (parking id: {self.id}, vehicle lp: {vehicle.getLicensePlate()})")
        self.is_occupied = True
        self.vehicle = vehicle
        return True
    
    def release_vehicle(self):
        if not self.is_occupied:
            print(f"WARNING: Tried to release vacant parking spot! (parking id: {self.id})")
            return False
        
        self.vehicle = None
        self.is_occupied = False
        return True


        
            