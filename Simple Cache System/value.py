from datetime import datetime, timedelta

class Value:
    def __init__(self, val, expiry):
        self.val = val
        self.expiry = datetime.now() + timedelta(seconds=expiry)
    
    def isExpired(self):
        return datetime.now() > self.expiry
    
    def getExpiry(self):
        return self.expiry
    
    def get(self):
        if self.isExpired():
            return None
        
        return self.val

    
