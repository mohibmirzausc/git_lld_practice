class ParkingLot:
    
    _instance = None

    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = ParkingLot()
        
        return cls._instance
    
