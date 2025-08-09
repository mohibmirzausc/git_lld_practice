# Simple Distributed Cache System with Expiry

## **Problem Statement**
Design a **distributed cache system** that meets the following requirements.

---

## **Basic Requirements**

### 1. Key-Value Storage
- Store **key-value pairs**.
- **Keys**: Unique strings.
- **Values**: Any serializable data type.
- Must support **updates** to existing values.

### 2. Expiry Time
- Each key-value pair has an **expiration time** (in seconds).
- Expired keys should be **automatically removed** from the cache.

### 3. Concurrency
- Cache must be **thread-safe** for concurrent read/write operations.
- Must prevent **race conditions** when accessing or modifying data.

### 4. Cache Eviction Policy
- Implement **Least Recently Used (LRU)** eviction.
- When cache reaches **maximum size**, remove the **least recently used** item.

### 5. Distributed Nature
- Simulate a **distributed cache**:
  - Multiple independent cache instances.
  - Each instance may hold **a subset of data**.
  - Instances should **synchronize** to share information about cached keys.

---

## **Methods to Implement**

### **`get(key)`**
- Returns value if:
  - Key exists **and** is not expired.
- Returns `None` otherwise.

### **`set(key, value, expiry)`**
- Adds or updates a key-value pair with an **expiry time** in seconds.
- If cache reaches size limit:
  - **Evict** least recently used item.

### **`remove(key)`**
- Removes the key-value pair for the given key.

### **`clear()`**
- Removes **all** data from cache.

### **`status()`**
- Returns:
  - Current cache size.
  - List of keys still stored.

---

## **Design Notes**

### Thread Safety
- Use **`threading.Lock`** or **`threading.RLock`** for safe concurrent access.

### Eviction Mechanism
- Use **`collections.OrderedDict`** to maintain **LRU order** efficiently.

### Distributed Cache Simulation
- Simulate communication between cache instances by:
  - Maintaining a **list of cache instances**.
  - Using a **shared resource** to exchange metadata about cached keys.

---

## **Implementation Goals**
- Efficient **key lookup**.
- Automatic **expiry handling**.
- **LRU eviction** when capacity is reached.
- **Concurrent access** without corruption.
- Simulation of **multi-instance distributed cache**.

---

## **Example Usage**

```python
# Create multiple cache instances
cache1 = DistributedCache(max_size=3)
cache2 = DistributedCache(max_size=3)

# Register instances for synchronization
DistributedCache.register_instance(cache1)
DistributedCache.register_instance(cache2)

# Set values with expiry
cache1.set("user:1", {"name": "Alice"}, expiry=10)
cache2.set("user:2", {"name": "Bob"}, expiry=5)

# Retrieve values
print(cache1.get("user:1"))
print(cache2.get("user:2"))

# Check cache status
print(cache1.status())
print(cache2.status())
