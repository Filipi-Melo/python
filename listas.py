'''Métodos das listas'''

lista:list[int]=[0,1,[2,3],3,4]
lista.append(4)
copy:list[int]=lista.copy()
lista.clear()

print(copy)
copy.remove(1)

copy2=copy.copy()
copy2[1][0]=6

print(copy)
print(copy2)
print(copy2.count(4))

copy2.extend(copy)
print(copy2)
print(copy2.index(4))

copy.insert(7,10)
print(copy)
print(copy.pop(1))

copy.extend([1,2,5,6,7,8,9])
copy.remove(4)
copy.reverse()
print(copy)

copy.sort()
print(copy)