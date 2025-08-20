import unittest

from ridestatus import RequestedStatus, AssignedStatus, StartedStatus, EndStatus

from trip import Trip

from rider import Rider

from ridetype import RideType
from ridestate import RideState
from location import Location
from driver import Driver

class TestSuite(unittest.TestCase):
    def setUp(self):
        print("setUp")

    def test_state_management(self):
        print("test_case")

        rider = Rider("Claire", "clairo@gmail.com")

        trip_builder = Trip.TripBuilder() \
            .set_rider(rider) \
            .set_ride_type(RideType.PREMIUM) \
            .set_pickup_location(Location(1, 1)) \
            .set_dropoff_location(Location(2, 5)) \
            .build()
        
        trip = Trip(trip_builder)
        
        self.assertEqual(trip.get_dropoff_location().x, 2)
        self.assertEqual(trip.get_pickup_location().y, 1)

        self.assertEqual(trip.get_state(), RideState.RequestedState)

        driver = Driver("Jake", "jake@hotmail.com", Location(9, 8))

        trip.assign(driver)

        self.assertEqual(trip.driver, driver)
        self.assertEqual(trip.get_state(), RideState.AssignedState)

        trip.start()
        self.assertEqual(trip.get_state(), RideState.StartState)

        trip.end()
        self.assertEqual(trip.get_state(), RideState.EndState)



    def tearDown(self):
        print("tearDown")

if __name__ == "__main__":
    unittest.main(verbosity=2)