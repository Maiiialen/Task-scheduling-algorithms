import copy

def moveSwap(osobnik, i, j):
    osobnik[i], osobnik[j] = osobnik[j], osobnik[i]

def func(lista):
    moveSwap(lista, 0, 3)

def func2(lista):
    listaNew = [9, 9, 9, 9, 9]
    lista = copy.deepcopy(listaNew)

lista1 = [1, 2, 3, 4, 5]
#moveSwap(lista1, 0, 2) # yes
#func(lista1) # ok
func2(lista1)

print(lista1)