import uuid
import heapq
from value import Value
from collections import OrderedDict

class Cache:
    def __init__(self, max_size=3):
        self.max_size = max_size
        self.uuid = uuid.uuid4()
        self.map = OrderedDict()
        self.pq = []

    def get(self, key):
        self.expireKeys()
        if key not in self.map:
            print(f"Warning: Cache Key Miss {key} : {self.uuid}")
            return None
        self.map.move_to_end(key)
        return self.map.get(key).get()

    def set(self, key, value, expiry): # expiry in seconds
        self.expireKeys()
        if len(self.map) >= self.max_size:
            self.map.popitem(last=False)
        
        if key in self.map:
            self.map.move_to_end(key)
        
        node = Value(value, expiry)
        self.map[key] = node
        heapq.heappush(self.pq, (node.getExpiry(), key))
        return True
    
    def expireKeys(self): 
        while self.pq:
            expiry, key = self.pq[0]
            node = self.map.get(key, None)

            if not node or node.getExpiry() != expiry:
                heapq.heappop(self.pq)
                continue
            if not node.isExpired():
                break
            
            heapq.heappop(self.pq)
            del self.map[key]

    
    def isFull(self):
        self.expireKeys()
        return len(self.map) >= self.max_size
    
    def size(self):
        self.expireKeys()
        return len(self.map)


        

        

        
        
        