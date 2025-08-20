from enum import Enum

class RideState(Enum):
    RequestedState = "Requested"
    AssignedState ="Assigned"
    StartState = "Start"
    EndState = "End"