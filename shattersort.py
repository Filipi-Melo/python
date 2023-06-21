from mylib import chain, drange, Iterable

def extend(array:list[list], size:int) -> None: 
    array.extend([] for _ in range(int(size)))

def iterator(array:list,stop) -> Iterable:
    return (array[i] for i in range(stop))

def ShatterPartition(array:list, length:int, num:int) -> None:
    if length < 2: return
    positives:list[list] = []
    negatives:list[list] = []

    for VAL in iterator(array,length):
        I:int = int(VAL // num)
        try:
            if I >= 0: positives[I].append(VAL)
            else: negatives[I].append(VAL)
        except IndexError:
            if I >= 0: 
                extend(positives, (max(iterator(array,length)) + 1) // num)
                positives[I].append(VAL)
            else: 
                extend(negatives, abs(min(iterator(array,length))) // num)
                negatives[I].append(VAL)
                
    array[:length] = chain.from_iterable(chain(negatives, positives))

def ShatterSort(array:list, length:int, num:int) -> None:
    shatters:int = int(length // num) + 1
    ShatterPartition(array, length, num)
    temp = [-1] * num

    for x in range(shatters):
        for y in range(num):
            if x * num + y < length: temp[y] = array[x * num + y]
        for val in temp:
            if x * num + (val % num) >= length or val == -1: break
            array[int(x * num + (val % num))] = val
    
def SimpleShatterSort(array:list, length:int, num:int, rate:int) -> None:
    for n in drange(num, 1, rate):
        ShatterPartition(array, length, n)
    ShatterPartition(array, length, 1)