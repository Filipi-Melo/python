from mylib import SafeInterrupt, sin, cos, sincos, xrange

A, B, C = 0, 0, 0
buffet:list[float] = []
matrix:list[str] = []
leng:int = 25 * 88
width, CubeWidth = 88, 16
Zb:float = 0

def insetcoo(x:int, y:int, z:int, char:str) -> None:
    idcoo:int = searchcoo(x, y, z)
    if idcoo >= 0 and idcoo <= len(matrix) and Zb > buffet[idcoo]:
        buffet[idcoo], matrix[idcoo] = Zb, char

@SafeInterrupt
def main() -> None:
    global matrix, buffet, A, B, C
    print("\x1b[2J")
    while True:
        matrix = [' '] * leng # ['█']
        buffet = [0.] * leng * 4
        for ix in xrange(-CubeWidth, CubeWidth, 0.8):
            for iy in xrange(-CubeWidth, CubeWidth, 0.8):
                values = (
                    [int(ix), int(iy), - CubeWidth, '#'], [-CubeWidth, int(iy), int(ix), '@'],
                    [CubeWidth, int(iy), int(ix), '%' ], [int(-ix), int(iy), CubeWidth, '='],
                    [int(ix), - CubeWidth, int(iy), '+'], [int(ix), CubeWidth, int(iy), '-']
                )
                for V in values: insetcoo(*V)
        print("\x1b[H", ''.join((matrix[i] if i % 88 else '\n') for i in range(len(matrix))))
        A += 0.05
        B += 0.05
        C += 0.02

def pitch(coox:int, cooy:int, cooz:int) -> float:
    sinA, cosA = sincos(A)
    sinB, cosB = sincos(B)
    sinC, cosC = sincos(C)
    return (cooy * cosA * cosC +
            cooz * sinA * cosC -
            cooy * sinA * sinB * sinC +
            cooz * cosA * sinB * sinC -
            coox * cosB * sinC)

def row(coox:int, cooy:int, cooz:int) -> float:
    sinA, cosA = sincos(A)
    sinB, cosB = sincos(B)
    sinC, cosC = sincos(C)
    return (cooy * sinA * sinB * cosC -
            cooz * cosA * sinB * cosC +
            cooy * cosA * sinC +
            cooz * sinA * sinC +
            coox * cosB * cosC)

def searchcoo(x:int, y:int, z:int) -> int:
    global Zb
    X:int = int(row(x, y, z)) + 44
    Y:int = int(pitch(x, y, z) / 2) + 12
    Zb = 1 / (yaw(x, y, z) + 100)
    return X + Y * width

def yaw(coox:int, cooy:int, cooz:int) -> float:
    cosB:float = cos(B)
    return (cooz * cos(A) * cosB -
            cooy * sin(A) * cosB +
            coox * sin(B))

if __name__ == '__main__': main()