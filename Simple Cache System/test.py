import unittest
import time
from value import Value
from cache import Cache
from distributedcache import DistributedCache

class TestLibrary(unittest.TestCase):
    def setUp(self):
        print("Setting up!")

    def test_value(self):
        val = Value("test", 2)
        self.assertFalse(val.isExpired())
        self.assertEqual(val.get(), "test")
        time.sleep(2)
        self.assertTrue(val.isExpired())
        self.assertEqual(val.get(), None)

    def test_cache(self):
        cache = Cache(3)
        cache.set("Jacket", 99, 2)
        self.assertTrue(cache.isFull, False)
        self.assertTrue(cache.size(), 1)
        self.assertTrue(len(cache.map), 1)
        self.assertTrue(len(cache.pq), 1)
        self.assertEqual(cache.map["Jacket"].val, 99)
        time.sleep(2)
        self.assertEqual(cache.map["Jacket"].get(), None)
        self.assertEqual(cache.get("Jacket"), None)

    def test_cache_overfill(self):
        cache = Cache(2)
        cache.set("Jacket", 99, 5)
        cache.set("Jeans", 135, 20)
        cache.set("Boots", 150, 20)
        self.assertEqual(cache.get("Jacket"), None)
        self.assertTrue(cache.get("Jeans"), 135)
        self.assertTrue(cache.get("Boots"), 150)

    def test_distributed_cache(self):
        d_cache = DistributedCache(2, 2, "abc")
        self.assertEqual(d_cache.get("test"), None)
        self.assertEqual(d_cache.set("address", "13214 Harcoro St.", 5), True)
        self.assertEqual(d_cache.set("groceries", "broccoli,kale,milk,chocolate", 5), True)
        self.assertEqual(d_cache.set("workout", "Pushup,Plank,Deadlift", 5), True)
        self.assertEqual(d_cache.set("random", 214, 5), True)
        self.assertEqual(d_cache.set("address2", "13214 Hare St", 5), True)

        self.assertEqual(d_cache.get("test"), None)
        self.assertEqual(d_cache.get("address"), None)
        self.assertEqual(d_cache.size(), 4) # fails sometimes due to hash salt
        



    

        

unittest.main(verbosity=2)