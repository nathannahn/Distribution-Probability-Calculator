import random

class Distribution:
    def __init__(self, size = 2):
        self._size = size
        self._buckets = [ListMapping() for i in range(self._size)]
        self._length = 0
        self._total = 0
        self.elements = []
        self.weights = []
        self.run = True

    def add(self, e, multiplicity = 1):
        m = self._bucket(e)
        if e in m:
            m[e] += multiplicity
        else:
            self._length += 1
            m[e] = multiplicity
        self._total += multiplicity
        self.run = True
            
        # Check if we need more buckets.
        if self._length > self._size:
            self._double()

    def count(self, e):
        m = self._bucket(e)
        return m[e]

    def prob(self, e):
        return (self.count(e) / self._total)
    
    def _bucket(self, key):
        return self._buckets[hash(key) % self._size]
    
    def _double(self):
#        print("I need more space!")
        # Save a reference to the old buckets.
        oldbuckets = self._buckets
        # Double the size.
        self._size *= 2
        # Create new buckets
        self._buckets = [ListMapping() for i in range(self._size)]
        # Add in all the old entries.
        for bucket in oldbuckets:
            for key, value in bucket.items():
                # Identify the new bucket.
                m = self._bucket(key)
                m[key] = value


    def bisearch(self, x, start = 0, end = 0):
        mid = (end - start)//2
    
        # If element is present at the middle itself 
        if self.sampler[mid][1] >= x and self.sampler[mid - 1][1] < x: 
            return mid 
          
        # If element is smaller than mid, then it can only 
        # be present in left subarray 
        elif self.sampler[mid][1] > x:
            return self.bisearch(x, start, mid-1) 
      
        # Else the element can only be present in right subarray 
        else: 
            return self.bisearch(x, mid+1, end) 

    def ceilingvalue(self, item):
        L = self.sampler
        left, right = 0, len(L)
        lstlen = right
        while right - left > 1:
            mid = (right + left)//2
            if item > L[mid][1]:
                left = mid
            else:
                right = mid
        if L[left][1] < item and right < lstlen:
            return L[right][0]
        else:
            return L[left][0]

    def sample(self):
        
        if self.run:
            self.sampler = []
            self.elements = []
            self.weights = []
            for lstMap in self._buckets:
                for e in lstMap:
                    for e in lstMap._entries:
                        if e.key not in self.elements:
                            self.elements.append(e.key)
                            self.weights.append(self.prob(e.key))
            self.run = False
            totalWeight = 0
            for i in range(len(self.elements)):
                totalWeight += self.weights[i]
                self.sampler.append((self.elements[i], totalWeight))

        x = random.randint(0,self._total)/self._total
        return self.ceilingvalue(x)
        
        
    def __len__(self):
        return self._length


# A class that stores key-value pairs
class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return str(self.key) + " : " + str(self.value)


# Implements the Mapping ADT:
# Stores the key-value pairs in a list
class ListMapping:
    def __init__(self):
        # Initialize an empty list to store the data
        self._entries = []

    # Add a new or update a key-value pair
    def put(self, key, value):
        e = self._entry(key)
        # If the key is present in the list
        if e is not None:
            # Update the value
            e.value = value
        else:
            # Else: Add it
            self._entries.append(Entry(key, value))
            
    # Access the value associated with a given key
    def get(self, key):
        e = self._entry(key)
        # If the key is found in the list
        if e is not None:
            # Return the associated value
            return e.value
        else:
            # Else: Raise a KeyError
            raise KeyError

    def _entry(self, key):
        for e in self._entries:
            if e.key == key:
                return e
        return None
    
    def __str__(self):
        return str([str(e) for e in self._entries])

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __len__(self):
        return len(self._entries)

    def __contains__(self, key):
        if self._entry(key) is None:
            return False
        else:
            return True

    def __iter__(self):
        return (e.key for e in self._entries)

    def values(self):
        return (e.value for e in self._entries)

    def items(self):
        return ((e.key, e.value) for e in self._entries)
