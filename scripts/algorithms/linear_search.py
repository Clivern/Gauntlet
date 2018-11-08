
#
# A simple approach is to do linear search, i.e
#
# - Start from the leftmost element of arr[] and one by one compare x with each element of arr[]
# - If x matches with an element, return the index.
# - If x doesn’t match with any of elements, return -1.

def search(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1
