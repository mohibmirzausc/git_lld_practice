import unittest
from vehiclefactory import VehicleFactory
from vehicle import Car, Truck

class TestSuite(unittest.TestCase):
    def setUp(self):
        print("Setting up tests...")

    def test_vehicle_factory(self): # factory design pattern
        car = VehicleFactory.create_vehicle("cAr", "NEED4SPEED")
        print(car)
        self.assertTrue(isinstance(car, Car))
        self.assertEqual(car.getSize(), 2)

        truck = VehicleFactory.create_vehicle("TRUCK", "GETOUT")
        self.assertTrue(isinstance(truck, Truck))
        self.assertEqual(truck.getSize(), 3)

    

unittest.main(verbosity=2)