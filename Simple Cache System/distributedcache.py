from cache import Cache
import string

class DistributedCache:

    def __init__(self, num_caches, cache_size, seed: string):
        self.caches = []
        for i in range(num_caches):
            self.caches.append(Cache(cache_size))
    
    def set(self, key, value, expiry):
        return self.caches[abs(hash(key)) % len(self.caches)].set(key, value, expiry)   

    def get(self, key):
        return self.caches[abs(hash(key)) % len(self.caches)].get(key)
    
    def size(self):
        sum = 0
        for i in range(len(self.caches)):
            sum += self.caches[i].size()
        return sum

    
