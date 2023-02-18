import timeit, numpy as np
from sorting import supersort

def loop_while():
    i=0
    while i< 100_000_000: i+=1
    return i

def loop_for():
    a=0
    for _ in range(100_000_000): a+=1
    return a

if __name__ == '__main__':
    print('for loop:   ',timeit.timeit(loop_for,number=1))
    print('while loop: ',timeit.timeit(loop_while,number=1))
    print('sum range:  ',timeit.timeit(lambda: sum(range(100_000_000)),number=1))
    print('sum numpy:  ',timeit.timeit(lambda: np.sum(np.arange(100_000_000)),number=1))
    print('math:       ',timeit.timeit(lambda n=100_000_000:(n*(n-1))/0.2,number=1))
    print('supersort:  ',timeit.timeit(lambda: supersort(range(100_000_000)),number=1))