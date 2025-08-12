from vehicle import Car, Bike, Truck

# Factory Design Pattern
class VehicleFactory:
    @staticmethod
    def create_vehicle(type, license_plate):
        if not isinstance(type, str):
            print("Pass a string in for type")
            return None
        
        type = str(type).lower()
        if type == "bike":
            return Bike(license_plate)
        elif type == "car":
            return Car(license_plate)
        elif type == "truck":
            return Truck(license_plate)
        else:
            print("Unrecognized Type")
            return None
        

        