'''Overload
=====
`function and method overload module.`

`Inspired in singledispatch.'''
from typing import Any, Callable, Generator, Generic, Iterable, ParamSpec, TypeVar

NULL:object = object()
T = TypeVar('T')
T2 = TypeVar('T2')
C = TypeVar('C')
P = ParamSpec('P')
P2 = ParamSpec('P2')

def getname(obj:Any) -> str:
    '`Returns the function or method name.'
    return str(obj).split()[1]

class Register(Generic[P,T]):
    '`Overloaded functions register class.'
    def __init__(sf, function:Callable[P,T], name:str) -> None:
        sf.overloads:list[Callable[P,T]] = [function]
        sf.name:str = name

    def __call__(sf, *args:P.args, **kwargs:P.kwargs) -> T:
        '`Looks up the function that matches the arguments.'
        total:int = len(args) + len(kwargs)
        if not total: return sf.overloads[-1]()

        groups:Generator = ((i, len(f.__defaults__ or []), f.__annotations__) for i,f in enumerate(sf.overloads))
        index:int = 0
        maxscore:int = 0

        for i, defaults, annotation in groups:
            length:int = len(annotation) - 1 if 'return' in annotation else len(annotation)            
            if length < total: continue
            score:int = (
                sum(map(instanceOf,args,annotation.values())) +
                sum(map(lambda key,value:key in annotation and instanceOf(value,annotation[key]), 
                        kwargs, kwargs.values()))
            )
            if score > maxscore: index, maxscore = i, score
            if length - defaults <= score == total: break

        return sf.overloads[index](*args,**kwargs)
    
    def register(sf, function:Callable[P2,T2]) -> Callable[P2,T2]:
        '`Registers the function and returns self or the function.'
        sf.overloads.append(function)
        return sf if sf.name == getname(function) else function

    def select(sf, index:int=NULL, param:Any=NULL, Return:Any=NULL) -> Callable[P,T]:
        '`Selects the specified overloaded function or method.'
        if index != NULL: return sf.overloads[index]

        pairs:list = [(f,f.__annotations__) for f in sf.overloads]        
        if Return != NULL:
            for function, annotation in pairs:
                if annotation.get('return',NULL) == Return: return function

        if param != NULL:
            for function, annotation in pairs:
                if param in annotation: return function

    def get(sf, instance:Any, objtype:Any=None) -> Callable[P,T]:
        '`Looks for the method that matches the arguments.'
        objt:tuple = (instance,) if instance != None else ()
        return lambda *args,**kwargs: sf(*objt + args, **kwargs)

setattr(Register, '__get__', Register.get)

class Overload:
    '`Decorator to easily overload functions and methods.'
    registers:dict[str, Register] = {}
    
    def __new__(cls,function:Callable[P,T]) -> Register[P,T]:
        if instanceOf(function,(property, staticmethod, classmethod)): raise TypeError(
            'Property, StaticMethod and ClassMethod cannot be overloaded.\n\t   '
            'Use Overload only in functions and methods.'
        )
        name:str = getname(function)
        if name in cls.registers: cls.registers[name].register(function)
        else: cls.registers.update({name:Register(function,name)})
        return cls.registers[name]

def instanceOf(Object:Any, Class:type|tuple) -> bool:
    '`Returns whether an object is an instance of a class without raising an TypeError.'
    try: return isinstance(Object, Class)
    except TypeError: return isinstance(Object,type(Class))

def main() -> None:
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
        from colorama import Style, Fore, init
        init(autoreset=True)    
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
