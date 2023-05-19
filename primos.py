from timeit import timeit

def primo(n:int) -> bool:
    if n < 2: return
    for i in range(2,int(1+abs(n)**0.5)): 
        if not n % i: break
    else: return True

def main(stop:int) -> None:
    primos:set = set()
    tempo:float = timeit(lambda: primos.update(filter(primo, range(2,stop))))
    print(f'Tempo: {tempo} s \nQuantidade de primos: {len(primos)}')
    
if __name__ == '__main__': main(int(1e6)) # n = 1e6 (1000000) -> 78498 primos