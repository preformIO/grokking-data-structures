from arrays.core import Array

# Store an instance of the int class with a value of 15 in a variable
n = 15
# Store an Array object from the the Array class definition
a = Array(n) # A (vector)

print(f"{n = }")
print(f"{a = }")

a[14] = 1000 # a[0] is a_0 / a term of A (vector)
a[0] = 20

print(f"{a = }")