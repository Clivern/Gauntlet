

def binarySearch(arr, leftE, rightE, target):

    # Check base case
    if rightE >= leftE:

        mid = int(leftE + (rightE - leftE)/2)

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

        # If element is smaller than mid, then it
        # can only be present in left subarray
        elif arr[mid] > target:
            return binarySearch(arr, leftE, mid-1, target)

        # Else the element can only be present
        # in right subarray
        else:
            return binarySearch(arr, mid+1, rightE, target)

    else:
        # Element is not present in the array
        return -1


def WorstCaseWithData(arr):
    return round(math.log(len(arr),2) + 1, 0)


def WorstCaseWithLenght(length):
    return round(math.log(length,2) + 1, 0)
