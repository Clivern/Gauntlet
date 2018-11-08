Data Structures and Algorithms
==============================


### Data Structures


---

### Algorithms


#### Binary search

```python
data = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97];
target = 67

# First Solution (a Linear Search)
def FirstSolution(data, target):
    i = 0
    steps = 0
    for item in data:
        if target == item:
            break
        i += 1
        steps += 1
    return {
        "result": i,
        "steps": steps
    }


# Second Solution (A binary Search)
def SecondSolution(data, target):
    steps = 0
    start = 0
    end = len(data)
    middle_position = int((start + end) / 2)
    middle_value = data[middle_position]

    while middle_value != target:
        if target > middle_value:
            start = middle_position + 1
        elif target < middle_value:
            end = middle_position - 1

        middle_position = int((start + end) / 2)
        middle_value = data[middle_position]
        steps += 1

    return {
        "result": middle_position,
        "steps": steps
    }


def WorstCaseWithData(data):
    return round(math.log(len(data),2) + 1, 0)

def WorstCaseWithLenght(length):
    return round(math.log(length,2) + 1, 0)


print(FirstSolution(data,target))
print(SecondSolution(data,target))
print(WorstCaseWithData(data))
print(WorstCaseWithLenght(len(data)))
```

### References

- [Algorithms by Khan Academy.](https://www.khanacademy.org/computing/computer-science/algorithms)
