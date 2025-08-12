import unittest
from vehicle import Vehicle, VehicleType, FuelType
from parkingstrategy import NoRestriction, RequiresSpotType, And, RequireVehicleType, FuelWhiteList
from spot import Spot
from passtype import PassType

class TestSuite(unittest.TestCase):
    def setUp(self):
        print("Setting up!")

    def test_no_restriction_parking(self):
        honda = Vehicle(VehicleType.CAR, FuelType.EV, PassType.PREMIUM)
        spot = Spot(VehicleType.CAR, NoRestriction())

        self.assertTrue(spot.can_park(honda))

    def test_valet_parking(self):
        honda = Vehicle(VehicleType.CAR, FuelType.EV, PassType.PREMIUM)
        spot = Spot(VehicleType.CAR, RequiresSpotType(PassType.VALET))

        self.assertFalse(spot.can_park(honda))

        toyota = Vehicle(VehicleType.CAR, FuelType.EV, PassType.VALET)
        self.assertTrue(spot.can_park(toyota))

    def test_strategy_and(self):
        honda = Vehicle(VehicleType.CAR, FuelType.EV, PassType.PREMIUM)
        spot = Spot(VehicleType.CAR, And(RequiresSpotType(PassType.PREMIUM), RequireVehicleType(VehicleType.CAR)))

        self.assertTrue(spot.can_park(honda))

        bike = Vehicle(VehicleType.BIKE, FuelType.EV, PassType.VALET)
        self.assertFalse(spot.can_park(bike))

    def test_whitelist_fuel_types(self):
        honda = Vehicle(VehicleType.CAR, FuelType.EV, PassType.PREMIUM)
        spot = Spot(VehicleType.CAR, FuelWhiteList(FuelType.EV))
        self.assertTrue(spot.can_park(honda))

        bike = Vehicle(VehicleType.BIKE, FuelType.Gasoline, PassType.VALET)
        self.assertFalse(spot.can_park(bike))

    def test_require_vehicle_type_multiple(self):
        car = Vehicle(VehicleType.CAR, FuelType.EV, PassType.PREMIUM)
        bike = Vehicle(VehicleType.BIKE, FuelType.Gasoline, PassType.VALET)
        truck = Vehicle(VehicleType.TRUCK, FuelType.Diesel, PassType.PREMIUM)
        allowed_types = [VehicleType.CAR, VehicleType.BIKE]
        spot = Spot(VehicleType.CAR, RequireVehicleType(allowed_types))
        self.assertTrue(spot.can_park(car))
        self.assertTrue(spot.can_park(bike))
        self.assertFalse(spot.can_park(truck))

    def test_fuel_whitelist_multiple(self):
        car_ev = Vehicle(VehicleType.CAR, FuelType.EV, PassType.PREMIUM)
        car_gas = Vehicle(VehicleType.CAR, FuelType.Gasoline, PassType.PREMIUM)
        car_diesel = Vehicle(VehicleType.CAR, FuelType.Diesel, PassType.PREMIUM)
        allowed_fuels = [FuelType.EV, FuelType.Gasoline]
        spot = Spot(VehicleType.CAR, FuelWhiteList(allowed_fuels))
        self.assertTrue(spot.can_park(car_ev))
        self.assertTrue(spot.can_park(car_gas))
        self.assertFalse(spot.can_park(car_diesel))

    def test_and_multiple_rules(self):
        car = Vehicle(VehicleType.CAR, FuelType.EV, PassType.PREMIUM)
        spot = Spot(VehicleType.CAR, And(
            RequiresSpotType(PassType.PREMIUM),
            RequireVehicleType([VehicleType.CAR, VehicleType.BIKE]),
            FuelWhiteList([FuelType.EV, FuelType.Gasoline])
        ))
        self.assertTrue(spot.can_park(car))
        bike = Vehicle(VehicleType.BIKE, FuelType.EV, PassType.PREMIUM)
        self.assertTrue(spot.can_park(bike))
        truck = Vehicle(VehicleType.TRUCK, FuelType.EV, PassType.PREMIUM)
        self.assertFalse(spot.can_park(truck))

    def test_or_strategy(self):
        car = Vehicle(VehicleType.CAR, FuelType.EV, PassType.PREMIUM)
        bike = Vehicle(VehicleType.BIKE, FuelType.Gasoline, PassType.VALET)
        from parkingstrategy import Or
        spot = Spot(VehicleType.CAR, Or(
            RequiresSpotType(PassType.VALET),
            RequireVehicleType([VehicleType.CAR, VehicleType.BIKE])
        ))
        self.assertTrue(spot.can_park(car))
        self.assertTrue(spot.can_park(bike))

    def test_and_empty_rules(self):
        car = Vehicle(VehicleType.CAR, FuelType.EV, PassType.PREMIUM)
        spot = Spot(VehicleType.CAR, And())
        self.assertTrue(spot.can_park(car))

    def test_or_empty_rules(self):
        car = Vehicle(VehicleType.CAR, FuelType.EV, PassType.PREMIUM)
        from parkingstrategy import Or
        spot = Spot(VehicleType.CAR, Or())
        self.assertFalse(spot.can_park(car))








        
        

unittest.main(verbosity=2)