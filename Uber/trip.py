from __future__ import annotations


from rider import Rider
from driver import Driver
from typing import Tuple, Optional
from ridetype import RideType
import uuid
from location import Location
from ridestate import RideState
from ridestatus import RideStatus, RequestedStatus

class Trip:
    def __init__(self, builder: Trip.TripBuilder):
        self.id = uuid.uuid4()
        self.rider = builder.rider
        self.pickup_location = builder.pickup_location
        self.dropoff_location = builder.dropoff_location
        self.ride_type = builder.ride_type
        self.driver = None
        self._status = RideState.RequestedState
        self.state = RequestedStatus()

    def assign(self, driver: Driver):
        self.state.assigned(self, driver)

    def start(self):
        self.state.start(self)

    def end(self):
        self.state.end(self)

    def get_driver(self) -> Driver:
        return self.driver

    def get_dropoff_location(self) -> Location:
        return self.dropoff_location
    
    def get_pickup_location(self) -> Location:
        return self.pickup_location
    
    def get_distance(self) -> int:
        return self.pickup_location.get_distance_to(self.dropoff_location)
    

    def get_state(self) -> RideState:
        return self._status
    
    def get_status(self) -> RideStatus:
        return self.state
    
    def set_state(self, trip_state: RideState):
        self._status = trip_state

    def set_status(self, status: RideStatus):
        self.state = status

    def set_driver(self, driver: Optional[Driver]):
        self.driver = driver

    
    

        
    class TripBuilder:
        def __init__(self):
            self.id = uuid.uuid4()
            self.rider: Optional[Rider] = None
            self.pickup_location: Optional[Location] = None
            self.dropoff_location: Optional[Location] = None
            self.ride_type: Optional[RideType] = None

        def set_rider(self, rider:Rider):
            self.rider = rider
            return self

        def set_pickup_location(self, pickup_location:Location):
            self.pickup_location = pickup_location
            return self

        def set_dropoff_location(self, dropoff_location:Location):
            self.dropoff_location = dropoff_location
            return self

        def set_ride_type(self, ride_type: RideType):
            self.ride_type = ride_type
            return self

        def build(self):
            if self.rider and self.pickup_location and self.dropoff_location and self.ride_type:
               return Trip(self)
            else:
                raise ValueError(f"Not all attributed set for trip builder (id='{self.id}')") 

