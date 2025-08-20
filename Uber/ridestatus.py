from __future__ import annotations

from abc import ABC, abstractmethod
from ridestate import RideState
from driverstatus import DriverStatus

class RideStatus(ABC):
    @abstractmethod
    def request(self, trip: 'Trip'): # waiting for driver
        pass
    
    @abstractmethod
    def assigned(self, trip: 'Trip', driver: 'Driver'): # assigned driver who is driving over
        pass
    
    @abstractmethod
    def start(self, trip: 'Trip'):
        pass

    @abstractmethod
    def end(self, trip: 'Trip'):
        pass

class RequestedStatus(RideStatus):
    def request(self, trip: 'Trip'):
        print("This ride has already been requested for!")

    def assigned(self, trip: 'Trip', driver: 'Driver'):
        trip.set_driver(driver)
        trip.set_state(RideState.AssignedState)
        trip.set_status(AssignedStatus())
        driver.set_status(DriverStatus.BUSY)
        print("Trip assigned successfully to a driver! ")

    def start(self, trip: 'Trip'):
        print("Cannot start trip that isn't assigned yet!")
        
    
    def end(self, trip: 'Trip'):
        print("Cannot end a trip that isn't assigned yet!")     

class AssignedStatus(RideStatus):
    def request(self, trip: 'Trip'):
        print("Ride already assigned!")

    def assigned(self, trip: 'Trip', driver: 'Driver'):
        print("Ride already assigned!")

    def start(self, trip: 'Trip'):
        trip.set_state(RideState.StartState)
        trip.set_status(StartedStatus())
        print("Ride successfully started!")

    def end(self, trip: 'Trip'):
        print("Cannot end ride that hasn't started!")

class StartedStatus(RideStatus):
    def request(self, trip: 'Trip'):
        print("This ride has already been requested for!")

    def assigned(self, trip: 'Trip', driver: 'Driver'):
        print("Trip already has been assigned!")

    def start(self, trip: 'Trip'):
        print("Cannot start ride that has already started!")
        
    def end(self, trip: 'Trip'):
        trip.set_status(EndStatus())
        trip.set_state(RideState.EndState)
        print("Trip has successfully ended!")       

class EndStatus(RideStatus):
    def request(self, trip: 'Trip'):
        print("Ride has already ended! Request anew!")

    def assigned(self, trip: 'Trip', driver: 'Driver'):
        print("Ride has ended! Cannot assign!")

    def start(self, trip: 'Trip'):
        print("Ride has ended! Cannot start!")

    def end(self, trip: 'Trip'):
        print("Ride has ended! Cannot end again!")