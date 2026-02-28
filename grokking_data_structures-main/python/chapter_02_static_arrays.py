from arrays.core import Array

# Store an instance of the int class with a value of 15 in a variable
n = 15
# Store an int (default) Array object from the the Array class definition
a = Array(n) # A (vector)


print(f"{n = }")
print(f"{a = }")

a[14] = 1000 # a[0] is a_0 / a term of A (vector)
a[0] = 20
# Uncomment line below to see TypeError result from trying to 
# store a float in an int array
# a[1] = 2.5 

print(f"{a = }")

print("Hello World!")

# Store an array of float data type
b = Array(5, 'f')
print(f"{b = }")
print(f"{b[2] = }")
b[3] = 3.1415

print(f"{b = }")

"""
A custom class definition for an unsorted array container
"""
class UnsorteArray:
    def __init__(self, max_size, typecode = 'l'):
        self._array = Array(max_size, typecode)
        self._max_size = max_size
        self._size = 0

    def insert(self, new_entry):
        if self._size >= len(self._array):
            raise ValueError('The array is already full')
        else:
            self._array[self._size] = new_entry
            self._size += 1
    
    def delete(self, index):
        if self._size == 0:
            raise ValueError('Delete from an empty array')
        elif not (0 <= index < self._size):
            raise ValueError(f'Index {index} out of range')
        else:
            self._array[index] = self._array[self._size-1]
            self._size -= 1
    
    def traverse(self, callback):
        for index in range(self._size):
            callback(self._array[index])

# Create an object (instance) from the UnsortedArray class
ua: UnsorteArray = UnsorteArray(n)
# Insert some numbers
ua.insert(0)
ua.insert(1)
ua.insert(25)

# Display it contents
print(f"{ua = }")
print(f"{ua._array = }")
print(f"{ua._size = }")
print("Traversing ua:")
ua.traverse(print)

# Remove the first number
ua.delete(0)
# Display its new contents
print("Traversing ua:")
print(f"{ua._array = }")
print(f"{ua._size = }")
ua.traverse(print)

