from abc import ABC, abstractmethod

class ParkingStrategy(ABC):
    @abstractmethod
    def can_park(self, spot: "Spot", vehicle: "Vehicle"):
        pass
    
    
    