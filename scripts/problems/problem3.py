
# https://www.hackerrank.com/challenges/list-comprehensions/problem

def XYZ():
    x = int(raw_input())
    y = int(raw_input())
    z = int(raw_input())
    n = int(raw_input())
    ar = []
    p = 0
    for i in range ( x + 1 ):
        for j in range( y + 1):
            for k in range( z + 1):
                if i+j+k != n:
                    ar.append([])
                    ar[p] = [ i , j, k ]
                    p+=1
    print ar


def XY():
    x = int(raw_input())
    y = int(raw_input())
    n = int(raw_input())
    ar = []
    p = 0
    for i in range ( x + 1 ):
        for j in range( y + 1):
            if i+j != n:
                ar.append([])
                ar[p] = [ i , j ]
                p+=1
    print ar