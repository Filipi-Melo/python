from typing import Any, Callable, Generic, ParamSpec, TypeVar

NULL:Any = object()
T = TypeVar('T')
T2 = TypeVar('T2')
P = ParamSpec('P')
P2 = ParamSpec('P2')

class Register(Generic[P,T]):
    overloads:list[Callable[P,T]]
    name:str
    def __init__(self, function:Callable[P,T], name:str) -> None:...
    def __call__(self, *args:P.args, **kwargs:P.kwargs) -> T:...
    def register(self, function:Callable[P2,T2]) -> Callable[P2,T2]:...
    def select(self, index:int=NULL, param:Any=NULL, Return:Any=NULL) -> Callable[P,T]:...
    def _get_(self, instance:Any, owner:Any=None) -> Callable[P,T]:... 

class Overload:
    registers:dict[str, Register]
    def __new__(cls, function:Callable[P,T]) -> Register[P,T]:...

def main() -> None:...