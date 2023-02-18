from timeit import timeit

def primo(n)-> bool:
    for i in range(2,int((n/2)+1)): 
        if n % i == 0: break
    else: return True

print('Tempo:',timeit(lambda:print('quantidade de primos:',len([i for i in range(2,250000) if primo(i)])),number=1),'s')