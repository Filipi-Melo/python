'''Overload
=====
`function and method overload module.`

`Inspired in singledispatch.'''
from typing import Any, Callable, Generator, Generic, Iterable, ParamSpec, TypeVar

NULL:object = object()
T = TypeVar('T')
T2 = TypeVar('T2')
P = ParamSpec('P')
P2 = ParamSpec('P2')

def getname(func:Callable) -> str:
    '`Returns the function or method name.'
    return f'{func.__module__}.{str(func).split()[1]}'
    
class RegisterList(list):
    (clear, copy, count, index, reverse, sort, __add__, __ge__,
    __gt__, __iadd__, __mul__, __le__, __lt__, __reversed__, __rmul__) = (None,) * 15

class Register(RegisterList,Generic[P,T]):
    '`Overloaded functions register class.'
    __slots__:tuple = 'name',
    def __init__(sf, function:Callable[P,T], name:str) -> None:
        sf.name:str = name
        sf.append(function)

    def __call__(sf, *args:P.args, **kwargs:P.kwargs) -> T:
        '`Looks up the function that matches the arguments.'
        total:int = len(args) + len(kwargs)
        if not total: return sf[-1]()
        index:int = 0
        maxscore:int = 0

        for i, defaults, length, annotation in sf.groups:
            if 'return' in annotation: length -= 1
            if length < total: continue
            score:int = (
                sum(map(instanceOf,args,annotation.values())) +
                sum(map(lambda key,value:key in annotation and instanceOf(value, annotation[key]), 
                        kwargs, kwargs.values()))
            )
            if score > maxscore: 
                index, maxscore = i, score
                if length - defaults <= score == total: break
        return sf[index](*args,**kwargs)
    
    @property
    def groups(sf) -> Generator[tuple[int, int, int, dict[str, type]], None, None]:
        return ((i, len(function.__defaults__ or []), len(function.__annotations__), 
                 function.__annotations__) for i, function in enumerate(sf))    
    
    def register(sf, function:Callable[P2,T2]) -> Callable[P2,T2]:
        '`Registers the function and returns self or the function.'
        sf.append(function)
        return sf if sf.name == getname(function) else function

    def select(sf, param:Any=NULL, Return:Any=NULL) -> Callable[P,T]:
        '`Selects the specified overloaded function or method.'
        pairs:list = [(func,func.__annotations__) for func in sf]        

        if Return != NULL:
            for function, annotation in pairs:
                if annotation.get('return', NULL) == Return: return function

        if param != NULL:
            for function, annotation in pairs:
                if param in annotation: return function
    
    def __get__(sf, instance:Any, owner:Any=None) -> Callable[P,T]:
        '`Looks for the method that matches the arguments.'
        obj:tuple = (instance,) if instance != None else ()
        return lambda *args,**kwargs: sf(*obj + args, **kwargs)
    
    def __repr__(sf) -> str:
        return f'Register({sf.name})'
    
    _get_ = __get__

class Overload:
    '`Decorator to easily overload functions and methods.'
    registers:dict[str, Register] = {}

    def __new__(cls, function:Callable[P,T]) -> Register[P,T]:
        if instanceOf(function,(property, staticmethod, classmethod)): raise TypeError(
            'Property, StaticMethod and ClassMethod cannot be overloaded. '
            'Use Overload only in functions and methods.'
        )
        name:str = getname(function)
        if name in cls.registers: cls.registers[name].append(function)
        else: cls.registers[name] = Register(function,name)
        return cls.registers[name]

def instanceOf(Object:Any, Class:type|tuple) -> bool:
    '`Returns whether an object is an instance of a class without raising an TypeError.'
    try: return isinstance(Object, Class)
    except TypeError: return isinstance(Object, type(Class))

def main() -> None:
    from colorama import Style, Fore, init
    init(autoreset=True)
    
    @Overload
    def test(*args:Any,**kwargs:Any) -> str:
        return 'test 1'
    @Overload
    def test(a:int,b:list,c:tuple) -> str:
        return 'test 2'
    @Overload
    def test(a:int,b:list,c:Iterable) -> str:
        return 'test 3'
    @test.register
    def _(a:float,b:list=[],c:None=None) -> str:
        return 'test 4'
    @test.register
    def _(a:None=None) -> str:
        return 'test 5'
    @test.register
    def _() -> str:
        return 'test 6'

    def tester(expected:str, function:Callable, *args, **kwargs) -> None:
        '`Tests the overloaded functions.'
        result:Any = function(*args, **kwargs)
        print(Style.BRIGHT + (f'{Fore.GREEN}The result match the expected:' if result == expected else
                              f'{Fore.RED}The result does not match the expected:'),
            f'\n{Style.BRIGHT}{result = }; {expected = }\n'
        )

    tester('test 1',test,'a','b','c',x=1,y=2.4,z=[],ඞ='ඞ')
    tester('test 3',test,40,(),[])
    tester('test 2',test,4,c=(),b=[])
    tester('test 4',test,2.0,(),None)
    tester('test 5',test,None)
    tester('test 6',test)

if __name__ == '__main__': main()