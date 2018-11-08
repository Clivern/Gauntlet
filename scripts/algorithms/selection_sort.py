
# 64 25 12 22 11
data = list(map(int, input().split(" ")))

def sort(arr):
    for i in range(len(arr)):
        # Find the smallest element after
        min_idx = i
        for j in range(i +1, len(arr)):
            if arr[min_idx] > arr[j]:
                min_idx = j

        # Swap the current element with the smallest one after
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

print(sort(data))

# Time Complexity: O(n2) as there are two nested loops.

# Auxiliary Space: O(1)
# The good thing about selection sort is it never makes more than O(n) swaps and can be useful when memory write is a costly operation.