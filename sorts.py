from mylib import Any, Callable, chain, Counter, Generator, SafeInterrupt, timer
from grailsort import GrailSortInPlace
from holygrailsort import HolyGrail, HolyShell
from shattersort import SimpleShatterSort, ShatterSort
from random import shuffle
from time import sleep
import numpy as np

def Bubble(array:list) -> list:
    LEN:int = len(array)
    for x in range(LEN):
        for y in range(x, LEN):
            if array[y] < array[x]: array[x], array[y] = array[y], array[x]
    return array

def CocktailShaker(array:list) -> list:
    END:int = len(array) - 1
    Sorted:bool = False
    while not Sorted:
        Sorted = True
        for x in reversed(range(1, END+1)):
            if array[x-1] > array[x]: array[x], array[x-1], Sorted = array[x-1], array[x], False
        if Sorted: break
        Sorted = True
        for y in range(END):
            if array[y] > array[y+1]: array[y], array[y+1], Sorted = array[y+1], array[y], False
    return array

def Comb(array:list) -> list:
    CONST:float = 1 / 1.247330950103979
    length:int = len(array)
    gap:int = length
    swapped:bool = True

    while gap > 1 or swapped:
        if gap > 1: gap = int(gap * CONST)
        swapped = False
        for i in range(length - gap):
            if array[i] > array[i + gap]:
                array[i], array[i + gap], swapped = array[i + gap], array[i], True
    return array

def Digit(num:int, place:int) -> int:
    return int(abs(num) / 10**place % 10)

def Gnome(array:list) -> list:
    i, j, LEN = 1, 2, len(array)
    while i < LEN:
        if array[i - 1] <= array[i]: i, j = j, j + 1
        else:
            array[i - 1], array[i], i = array[i], array[i - 1], i - 1
            if not i: i, j = j, j + 1
    return array

def Heap(array:list) -> list:
    END:int = len(array) - 1
    mid:int = (END - 1) // 2
    Heapify(array, mid + 1, END)

    for i in reversed(range(1, END + 1)):
        array[0], array[i] = array[i], array[0]
        SiftDown(array, 0, i - 1)
    return array

def Heapify(array:list,start,end) -> None:
    for i in reversed(range(start)): SiftDown(array, i, end)

def HeapInsertion(array:list) -> list:
    END:int = len(array) - 1
    mid:int = (END - 1) // 2
    Heapify(array, mid + 1, END)

    for i in reversed(range(END)):
        left:int = i
        temp = array[i]
        if array[i + 1] > temp: continue
        if array[END] < temp: 
            array.insert(END, array.pop(i))
            continue        
        
        while array[i + 1] <= temp: i += 1
        array.insert(i, array.pop(left))
    return array

def Insertion(array:list) -> list:
    for x, VAL in enumerate(array, -1):
        while x >= 0 and VAL < array[x]: 
            array[x + 1] = array[x]
            x -= 1
        array[x + 1] = VAL
    return array

def Merge(left:list, right:list) -> list:
    def merged() -> Generator[Any, None, None]:
        while left and right: yield left.pop(0) if left[0] <= right[0] else right.pop(0)
    return [*merged(), *left, *right]

def MergeSort(array:list) -> list:
    if len(array) < 2: return array
    MID:int = len(array) // 2
    return Merge(MergeSort(array[:MID]), MergeSort(array[MID:]))

def NumpySort(List:list) -> np.ndarray:
    NEW = np.array(List)
    NEW.sort()
    return NEW

def Quick(array:list, left:int = 0, right:int|None = None) -> list:
    right = right if right != None else len(array) - 1
    if left >= right: return array

    PIVOT, ind = array[right], left
    for i in range(left, right):
        if array[i] < PIVOT: array[i], array[ind], ind = array[ind], array[i], ind + 1
    array[right], array[ind] = array[ind], array[right]

    try:
        Quick(array, left, ind - 1)
        Quick(array, ind + 1, right)
    finally: return array

def QuickCheater(array:list) -> list:
    if len(array) < 2: return array
    Iter = iter(array)
    PIVOT:Any = next(Iter)
    left:list = []
    right:list = []

    for v in Iter:
        if v < PIVOT: left.append(v)
        else: right.append(v)
    return [*QuickCheater(left), PIVOT, *QuickCheater(right)]

def RadixSort(array:list) -> list:
    # from math import log10
    # def NumberOfDigits(num):
    #     return int(log10(abs(num)) if num else 0) + 1
    # MAX = NumberOfDigits(max(array)) # Slow
    MAX:int = len(str(max(array)))
    Len = len(array)
    for i in range(MAX):
        buckets:list[list] = [[] for _ in range(10)]
        for val in array: buckets[Digit(val, i)].append(val)        
        array[:Len] = chain.from_iterable(buckets)
    return array

def Seletion(array:list) -> list:
    LEN:int = len(array)
    for x in range(LEN):
        Min:int = x
        for y in range(x + 1,LEN):
            if array[y] < array[Min]: Min = y
        if x != Min: array[x], array[Min] = array[Min], array[x]
    return array

def SeletionCheater(array:list) -> list:
    def select(temp:list):
        while temp: yield temp.pop(temp.index(min(temp)))
    return [*select(array.copy())]

def Shell(array:list) -> list:
    LEN:int = len(array)
    gap:int = LEN // 2
    while gap:
        for x in range(gap, LEN):
            VAL:Any = array[x]
            x -= gap
            while x >= 0 and VAL <= array[x]:
                array[x + gap] = array[x]
                x -= gap
            array[x + gap] = VAL
        gap //= 2
    return array

def SiftDown(array:list, start:int, end:int) -> None:
    while 2 * start + 1 <= end:
        child, toSwap = start * 2 + 1, start
        if array[toSwap] < array[child]: toSwap = child
        if child + 1 <= end and array[toSwap] < array[child + 1]: toSwap = child + 1 
        if toSwap == start: return
    
        array[start], array[toSwap], start = array[toSwap], array[start], toSwap

ALL:dict[str,Callable] = {
    'Bubble': Bubble,
    'Cocktail Shaker': CocktailShaker,
    'Comb': Comb,
    'Gnome': Gnome,
    'Grail': lambda arr: GrailSortInPlace(arr,0,len(arr)),
    'Heap': Heap,
    'Heap Insertion': HeapInsertion,
    'Holy Grail': HolyGrail,
    'Holy Shell': HolyShell,
    'Insertion': Insertion,
    'Merge': MergeSort,
    'Numpy arange': lambda arr: np.arange(len(arr),0,-1).sort(),
    'Numpy array': NumpySort,
    'Python Tim': lambda arr: arr.sort(),
    'Quick': Quick,
    'Quick Cheater': QuickCheater,
    'Radix': RadixSort,
    'Seletion': Seletion,
    'Seletion Cheater': SeletionCheater,
    'Shatter':lambda arr: ShatterSort(arr,len(arr),1),
    'Shell': Shell,
    'Simple Shatter':lambda arr: SimpleShatterSort(arr,len(arr),0,0)
}

SCORES:Counter[str] = Counter()

def time(function:Callable, copy:list, name:str) -> float: 
    print(name,'sort...')
    return timer(lambda: function(copy))

@SafeInterrupt
def loop(array:list, repeat:int, delay:float) -> None:
    for step in range(repeat):
        print('Shuffling...')
        shuffle(array)
        print(f'Starting >>>>> Step:{step + 1}\n')

        results:dict[float,str] = { time(ALL[key], array.copy(), key):key for key in ALL }
        times:list = Shell([*results])[::-1]
        SCORES[results[times[-1]].replace('  ','')] += 1

        print(
            f"\n{'Results':=^50}\n", 
            '\n'.join(f"{(results[sec]+' sort:'):<30} {sec:.6f} s" for sec in times),'\n',
            sep=''
        )
        sleep(delay)

def main(length:float, repeat:int=1, delay:float=0.1) -> None:
    array:list = [*range(int(length))]

    print(f"{f'List size: {int(length)}':_^50}")
    loop(array, repeat, delay)
    print(f"{'Fastest':_^50}\n",
        '\n'.join(f"{(KEY+' sort:'):<31}{SCORES[KEY]}" for KEY in ALL),
        sep=''
    )

if __name__ == '__main__': main(8192)