from rider import Rider
from driver import Driver
from typing import Tuple, Optional
from ridetype import RideType
import uuid
from location import Location

from __future__ import annotations

class Trip:
    def __init__(self, builder: Trip.TripBuilder):
        self.id = uuid.uuid4()
        self.rider = builder.rider
        self.driver = builder.driver
        self.pickup_location = builder.pickup_location
        self.dropoff_location = builder.dropoff_location
        self.ride_type = builder.ride_type

    def get_dropoff_location(self):
        return self.dropoff_location
    
    def get_pickup_location(self):
        return self.pickup_location
        
    class TripBuilder:
        def __init__(self):
            self.id = uuid.uuid4()
            self.rider: Optional[Rider] = None
            self.driver: Optional[Driver] = None
            self.pickup_location: Optional[Location] = None
            self.dropoff_location: Optional[Location] = None
            self.ride_type: Optional[RideType] = None

        def set_rider(self, rider:Rider):
            self.rider = rider
            return self

        def set_driver(self, driver:Driver):
            self.driver = driver
            return self

        def set_pickup_location(self, pickup_location:Tuple):
            self.pickup_location = pickup_location
            return self

        def set_dropoff_location(self, dropoff_location:Tuple):
            self.dropoff_location = dropoff_location
            return self

        def set_ride_type(self, ride_type: RideType):
            self.ride_type = ride_type
            return self

        def build(self):
            if self.rider and self.driver and self.pickup_location and self.dropoff_location and self.ride_type:
               return Trip(self)
            else:
                raise ValueError(f"Not all attributed set for trip builder (id='{self.id}')") 

