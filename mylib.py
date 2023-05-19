from typing import Any, Callable, Generator, Iterable
from collections import Counter
from Overload import Overload
from numpy import arange as xrange
from math import sin, cos

def chain(*iterables,**kw) -> Generator[Any, None, None]:
    '`Chain iterables until all iterables are exhausted.'
    Iterables:Iterable = kw['iterables'] if 'iterables' in kw else iterables
    for iterable in Iterables: yield from iterable

@Overload
def Copy(array1:list, pos1:int, array2:list, pos2:int, length:int) -> None:
    if length < 0: return
    for i, VAL in enumerate(array1[pos1:length+pos1]): array2[i+pos2] = VAL

@Overload
def Copy(array1:tuple, pos1:int, array2:list, pos2:int, length:int) -> None: 
    if length < 0: return
    for i, VAL in enumerate(array1[pos1:length+pos1]): array2[i+pos2] = VAL

@Overload
def Copy(iterable:Iterable, pos1:int, array:list, pos2:int, length:int) -> None: 
    if length < 0: return
    for i,VAL in filter(lambda t:t[0]>=pos1, enum(iterable, length)): array[i+pos2] = VAL

@Overload
def Copy(iterable:Iterable, array:list, pos:int, length:int) -> None:
    if length < 0: return
    for i,VAL in enum(iterable, length): array[i+pos] = VAL

@Overload
def drange(start:float, stop:float, step:float) -> Generator[float, None, None]: 
    if 1 >= abs(step) >= 0: return
    while start > stop:
        yield start
        start /= step

@Overload
def drange(start:int, stop:int, step:float) -> Generator[int, None, None]:
    if 1 >= abs(step) >= 0: return
    while start > stop:
        yield start
        start = int(start//step)

def enum(iterable:Iterable,length:int,start:int=0) -> Generator[tuple[int, Any], None, None]:
    '`Can enumerate all iterable types.'
    yield from zip(range(start,length),iterable)

def Interrupt(function:Callable) -> Callable:
    '`Decorator to safely cancel functions using keyboard.'
    def wrapper(*args,**kwargs) -> Any:
        try: return function(*args,**kwargs)
        except KeyboardInterrupt: pass
    return wrapper

def mrange(start:int|float, stop:int|float, step:int|float) -> Generator[int|float, None, None]:
    if not step: return
    while start < stop:
        yield start
        start *= step

def powrange(start:int|float, stop:int|float, step:int|float) -> Generator[int|float, None, None]:
    while start < stop:
        yield start
        start **= step

def sincos(num:float) -> tuple[float, float]: 
    return sin(num), cos(num)