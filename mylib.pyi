from typing import overload, TYPE_CHECKING
from overload import Register
from _mylib import *

T = TypeVar('T')
P = ParamSpec('P')

if TYPE_CHECKING:
    T2 = TypeVar('T2')

    def union(f1:T, f2:T2) -> Callable[...,T|T2]:...
    def _R(f:Callable[P,T]) -> Register[P,T]:...
    @_R
    def _ArrayCopy1(array1:list, pos1:int, array2:list, pos2:int, length:int) -> None:
        '`Copy the values of an list to another list.'
    @_R
    def _ArrayCopy2(array1:tuple, pos1:int, array2:list, pos2:int, length:int) -> None:
        '`Copy the values of an tuple to the list.'
    @_R
    def _ArrayCopy3(iterable:Iterable, array:list, pos:int, length:int) -> None:
        '`Copy the values of an iterable to the list.'
    @_R
    def _drange1(start:int, stop:int, step:float) -> Generator[int, None, None]:...
    @_R
    def _drange2(start:float, stop:float, step:float) -> Generator[float, None, None]:...

@union(_ArrayCopy1, union(_ArrayCopy2, _ArrayCopy3)())
def ArrayCopy():...

@union(_drange1, _drange2)
def drange():...

def enum(iterable:Iterable[T], length:int, start:int=0) -> Generator[tuple[int, T], None, None]:...

def fillArray(array:list, value:Any, start:int=0, stop:int|None=None) -> None:...

class FilterMap:
    def __new__(cls, Map:Callable, *iterables:Iterable[T], Filter:Callable|None=None) -> Generator[T,None,None]:...

class Flat: 
    def __new__(cls, iterable:Iterable[T]) -> Generator[T,None,None]:...

def instanceOf(Object:Any,Class:type|tuple[type,...]) -> bool:...

@overload
def mrange(start:int, stop:int, step:int) -> Generator[int, None, None]:...
@overload
def mrange(start:float, stop:float, step:float) -> Generator[float, None, None]:...

@overload
def powrange(start:int, stop:int, step:int) -> Generator[int, None, None]:...
@overload
def powrange(start:float, stop:float, step:float) -> Generator[float, None, None]:...

def SafeInterrupt(function:Callable[P,T]) -> Callable[P,T]:...

def sincos(num:float) -> tuple[float, float]:...

def timer(function:Callable) -> float:...

def zipdicts(*dicts:dict,fill:Any=None):...