"""
Cole Detrick
Student ID:011447776
"""

class CreateHashMap:
    def __init__(self, initial_capacity=20):
        self.list = [[] for _ in range(initial_capacity)]
# Custom hash function which utilizes bit manipulation and collision handling
    def _hash_function(self, key):
        hash_value = 0
        for char in str(key):
            hash_value = (hash_value << 5) + ord(char)
        return hash_value % len(self.list)
# This will insert a new element or updates an existing element in the hash table
    def insert(self, key, item):
        bucket = self._hash_function(key) # applies hash function with the key
        bucket_list = self.list[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        bucket_list.append([key, item]) # if the constraints are met, appends item to end of our list
        return True

# this function enables you to lookup elements in the hash table
    def lookup(self, key):
        bucket = self._hash_function(key)
        bucket_list = self.list[bucket]
        for pair in bucket_list:
            if key == pair[0]:
                return pair[1]
        return None
# removes an existing item in the hash table
    def hash_remove(self, key):
        bucket = self._hash_function(key)
        bucket_list = self.list[bucket]
        for i, pair in enumerate(bucket_list):
            if pair[0] == key:
                bucket_list.pop(i)
                return True
        return False