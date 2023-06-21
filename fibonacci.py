def seq_fib(num:int) -> None:
    if num < 1: return print(num)
    a, b = 0, 1
    for _ in range(num):
        a, b = b, a + b
        print(f'{a} + {b} = {a + b}')

if __name__ == '__main__': 
    seq_fib(int(input("Digite o limite da sequência: ")))