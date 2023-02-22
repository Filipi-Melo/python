from numpy import arange, array
from random import shuffle
from timeit import timeit

def supersort(Array): 
    '`Fake sort`'
    return range(len(Array))

def npsort(Array:list) -> list:
    _array = array(Array)
    _array.sort()
    return _array

def sort(array:list) -> list:
    '''`Seletion sort.`

    `Cresce em progressão aritmética.`
    
    `número de comparações = ((1+n)*n)/2`
    '''
    for x in range(len(array)-1,0,-1):
        for y in range(x):
            if array[x] < array[y]: array[x], array[y] = array[y], array[x]
    return array

if __name__ == '__main__':
    print('Criando...')
    size = 10_000_000
    Array, test = list(range(size)),list(range(10000))
    
    print('Shuffled: ',timeit(lambda: (shuffle(Array), shuffle(test)), number=1),' s')
    a1,a2,a3 = [Array.copy() for _ in range(3)]

    print('Começou! Tamanho: ',size,'\n----------------------------')
    
    print('sort:                ',timeit(lambda: sort(test), number=1),' s') # lento
    print('python in-place sort:',timeit(lambda: a1.sort(), number=1),' s')
    print('numpy sort:          ',timeit(lambda: npsort(a2), number=1),' s')
    print('numpy array sort:    ',timeit(lambda: array(arange(size,0,-1)).sort(), number=1),' s')
    print('numpy arange sort:   ',timeit(lambda: arange(size,0,-1).sort(), number=1),' s')
    print('Supersort list:      ',timeit(lambda: supersort(a3), number=1),' s')
    print('Supersort range:     ',timeit(lambda: supersort(range(size)), number=1),' s')