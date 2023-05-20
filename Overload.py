from typing import Any, Callable, Generator, Iterable

NULL:object = object()

class Register:
    '`Overloaded functions register class.'
    def __init__(sf,function:Callable) -> None:
        sf.overloads:list[Callable] = [function]
        sf.name:str = function.__name__

    def __call__(sf, *args: Any, **kwargs: Any) -> Any:
        '`Looks up the function that matches the arguments.'
        groups:Generator = ((i,len(f.__defaults__ or []),f.__annotations__) for i,f in enumerate(sf.overloads))
        scores:list[int] = [0] * len(sf.overloads)
        total:int = len(args) + len(kwargs)
        if not total:
            for i,length in ((i,len(ann)-1 if 'return' in ann else len(ann)) for i,_,ann in groups):
                if not length: return sf.overloads[i]()
            return sf.overloads[0]()

        for i,defaults,annotation in groups:
            length:int = len(annotation)-1 if 'return' in annotation else len(annotation)
            if length < total: continue
            scores[i] = (
                sum(map(instanceOf,args,annotation.values())) +
                sum(map(lambda key,value:key in annotation and instanceOf(value,annotation[key]),kwargs,kwargs.values()))
            )
            if length - defaults <= scores[i] == total: return sf.overloads[i](*args,**kwargs)
        return sf.overloads[scores.index(max(scores))](*args,**kwargs)
    
    def register(sf,function:Callable) -> Callable:
        '`Registers the function and returns self or the function.'
        sf.overloads.append(function)
        return sf if sf.name == function.__name__ else function

    def select(sf,index:int=NULL,param:Any=NULL,Return:Any=NULL) -> Callable:
        '`Selects the specified overloaded function.'
        if index != NULL: return sf.overloads[index]        
        for function,annotation in ((f,f.__annotations__) for f in sf.overloads):
            if Return != NULL and annotation.get('return',NULL) == Return or \
                param != NULL and param in annotation: return function

class Overload:
    '''`Decorator to easily overload functions and methods.`

    `Inspired in singledispatch.'''
    registers:dict[str,Register] = {}
    def __new__(cls,function:Callable) -> Register:
        name:str = function.__name__
        if name in cls.registers: cls.registers[name].register(function)
        else: cls.registers.update({name:Register(function)})
        return cls.registers[name]

def instanceOf(Object:Any,Class:Any) -> bool:
    '`Returns whether an object is an instance of a class without raising an TypeError.'
    try: return isinstance(Object,Class)
    except TypeError: return isinstance(Object,type(Class))

def tester(expected:str,function:Callable,*args,**kwargs) -> None:
    '`Tests the overloaded functions.'
    from colorama import Style, Fore, init
    init(autoreset=True)
    result:Any = function(*args,**kwargs)
    print(Style.BRIGHT + f'{Fore.GREEN}The result match the expected:' if result == expected 
          else f'{Fore.RED}The result does not match the expected:',
        f'\n{Style.BRIGHT}{result = }; {expected = }\n'
    )

def main():
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
    
    tester('test 1',test,10,[],(),x=1,y=3,z=[],ඞ='ඞ')
    tester('test 3',test,40,(),[])
    tester('test 2',test,4,c=(),b=[])
    tester('test 4',test,2.0,[],None)
    tester('test 5',test,None)
    tester('test 6',test)

if __name__ == '__main__': main()