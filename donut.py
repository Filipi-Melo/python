from mylib import xrange, sincos, SafeInterrupt

@SafeInterrupt
def main() -> None:
    A:float = 0
    B:float = 0
    print("\x1b[2J")
   
    while True:
        b:list[str] = [(" " if k % 80 else "\n") for k in range(1760)]
        Z:list[float] = [0] * 1760
        sA, cA = sincos(A)
        sB, cB = sincos(B)
        
        for st, ct in map(sincos, xrange(0, 6.28, 0.07)):
            for sp, cp in map(sincos, xrange(0, 6.28, 0.02)):
                H:float = ct + 2
                D:float = 1 / (sp * H * sA + st * cA + 5) 
                T:float = sp * H * cA - st * sA
                X:int = int(40 + 30 * D * (cp * H * cB - T * sB))
                Y:int = int(12 + 15 * D * (cp * H * sB + T * cB))
                N:int = int(8 * ((st * sA - sp * ct * cA) * cB - sp * ct * sA - st * cA - cp * ct * sB))
                O:int = X + 80 * Y
                if O > 1759: continue
                if Y < 22 and Y >= 0 and X >= 0 and X < 79 and D > Z[O]:
                    Z[O] = D
                    b[O] = ".,-~:;=!*#$@"[int(N) if N > 0 else 0]
        
        print("\x1b[H\n",''.join(b), sep='')
        A += 0.07
        B += 0.04

if __name__ == '__main__': main()