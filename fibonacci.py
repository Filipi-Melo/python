def seq_fib(num):
    if num < 1: return print(num)
    a,b = 0,1
    for _ in range(num):
        a,b=b,a+b
        print(a," + ",b," = ",a+b)
    
seq_fib(int(input("Digite o limite da sequência: ")))