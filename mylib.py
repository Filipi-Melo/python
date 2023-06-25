from typing import Any, Callable, Counter, Generator, Iterable, TypeVar, ParamSpec
from numpy import arange as xrange
from math import sin, cos
from overload import Overload
from timeit import timeit
from traceback import print_exception as printTraceback
from itertools import chain

T = TypeVar('T')
P = ParamSpec('P')

@Overload
def ArrayCopy(array1:list, pos1:int, array2:list, pos2:int, length:int) -> None:
    '`Copy the values of an list to another list.'
    if length < 1: return
    array2[pos2:length + pos2] = array1[pos1:length + pos1]

@Overload
def ArrayCopy(array1:tuple, pos1:int, array2:list, pos2:int, length:int) -> None: 
    '`Copy the values of an tuple to the list.'
    if length < 1: return
    array2[pos2:length + pos2] = array1[pos1:length + pos1]

@Overload
def ArrayCopy(iterable:Iterable, array:list, pos:int, length:int) -> None:
    '`Copy the values of an iterable to the list.'
    if length < 1: return
    array[pos:length + pos] = iterable

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
        start = int(start // step)

def enum(iterable:Iterable[T], length:int, start:int=0) -> Generator[tuple[int, T], None, None]:
    '`Returns an enumeration generator for all iterable types.'
    yield from zip(range(start,length),iterable)

def fillArray(array:list, value:Any, start:int=0, stop:int|None=None) -> None:
    '`fills an list.'
    if stop == None: stop = len(array)
    array[start:stop] = (value for _ in range(start, stop))

class FilterMap:
    '`Returns an iterator for filtering and mapping at the same time.'
    def __new__(cls, Map:Callable, *iterables:Iterable[T], Filter:Callable|None=None) -> Generator[T,None,None]:
        yield from filter(Filter, map(Map, *iterables))

class Flat:
    '`Class to flatten any iterable.'
    def __new__(cls, iterable:Iterable[T]) -> Generator[T,None,None]:
        if instanceOf(iterable, str): 
            yield from iterable
            return
        
        for value in iterable:
            if instanceOf(value, Iterable): yield from Flat(value) 
            else: yield value

def instanceOf(Object:Any,Class:type|tuple[type]) -> bool:
    '`Returns whether an object is an instance of a class without raising an TypeError.'
    try: return isinstance(Object,Class)
    except TypeError: return isinstance(Object,type(Class))

def SafeInterrupt(function:Callable[P,T]) -> Callable[P,T]:
    '`Decorator to safely cancel functions using keyboard.'
    def wrapper(*args:P.args,**kwargs:P.kwargs) -> T:
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

def timer(function:Callable) -> float:
    '`Calls the timeit once.'
    return timeit(function, number=1)

def zipdicts(*dicts:dict,fill:Any=None):
    '`Zips keys and dicts values.'
    if not dicts: return
    for key in chain(dicts): 
        yield key, *(Dict.get(key, fill) for Dict in dicts)