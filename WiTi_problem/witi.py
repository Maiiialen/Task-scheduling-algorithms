import copy
import math
import timeit
from itertools import permutations

def loadData(path):
    plik = open(path, "r")
    linie = plik.readlines()
    n = int(linie[0].split()[0])

    zadania = []
    for i in range(1, n+1):
        linia = linie[i].split()
        zadania.append([int(linia[0]),int(linia[1]),int(linia[2]), i])
    plik.close()

    return zadania

def calculate_Fmax(zad):
    S = []  # momenty rozpoczecia
    C = []  # momenty zakonczenia
    T = []  # spoznienie zadania
    Fmax = 0

    S.append(0)                         # S(0) = 0
    C.append(zad[0][0])                 # C(0) = p_zad0
    T.append(max(C[0]-zad[0][2],0))     # T = 0 lub T = C_zad0 - d_zad0
    Fmax = zad[0][1] * T[0]             # F_zad0 = w_zad0 * T_zad0
    for j in range(1, len(zad)):        # i tak samo dla reszty zadan
        S.append(C[j-1])
        C.append(S[j] + zad[j][0])
        T.append(max(C[j]-zad[j][2],0))
        Fmax += zad[j][1] * T[j]

    return Fmax
    
def sortD(zad):
    while True:
        zmiana = False
        for j in range(0, len(zad)-1):
            if zad[j][2] > zad[j+1][2]:
                zad[j], zad[j+1] = zad[j+1], zad[j]
                zmiana = True

        if zmiana == False:
            return zad

def optPermutations(zad):
    perms = list(permutations(zad,r=len(zad)))  # lista wszystkich mozliwych permutacji o dlugosci n
    Fmax = math.inf
    for perm in perms:
        F = calculate_Fmax(perm)
        if F < Fmax:
            Fmax = F
    return Fmax

def optRecursionStart(zad):
    availableTasks = copy.deepcopy(zad)
    currentTasks = []
    Fmax = math.inf
    n = len(zad)

    def optRecursion(zad, current):
        nonlocal Fmax
        nonlocal n
        availableTasks = copy.deepcopy(zad)
        currentTasks = copy.deepcopy(current)

        if len(zad) != 0 and currentTasks != n:
            for i in range(0, len(availableTasks)):
                currentTasks.append(copy.copy(availableTasks[i]))
                temp = availableTasks.pop(i)
                optRecursion(availableTasks, currentTasks)
                availableTasks.insert(i, temp)
                currentTasks.pop()
        else:
            F = calculate_Fmax(copy.deepcopy(currentTasks))
            if F < Fmax:
                Fmax = F

    optRecursion(availableTasks, currentTasks)
    return Fmax

def dynamicIterations(zad):
    availableTasks = copy.deepcopy(zad)
    currentTasks = []
    knownValues = {}
    Fmin = math.inf

    for i in range(1, 2**len(zad)):
        binTasksToCheck = bin(i).replace("0b","")
        if binTasksToCheck not in knownValues:
            iterator = 0
            for binChar in reversed(binTasksToCheck):
                if binChar == '1':
                    currentTasks.append(availableTasks[iterator])
                iterator = iterator + 1

            sumOfP = pSum(copy.deepcopy(currentTasks))
            Fmin = math.inf
            iterator = 0
            binIterator = 0
            for binChar in reversed(binTasksToCheck):
                if binChar == '1':
                    binChecking = list(reversed(binTasksToCheck))
                    binChecking[binIterator] = '0'
                    binChecking.reverse()
                    cutBinChecking = []
                    for k in range(0, len(binChecking)):
                        if binChecking[k] == '1':
                            cutBinChecking = binChecking[k:len(binChecking)]
                            break
                    binChecking = ''.join(cutBinChecking)
                    
                    F = max((sumOfP - currentTasks[iterator][2]), 0) * currentTasks[iterator][1]
                    if binChecking in knownValues:
                        F += knownValues[binChecking]
                    if F < Fmin:
                        Fmin = F
                    iterator = iterator + 1
                binIterator = binIterator + 1
                    
            knownValues[binTasksToCheck] = Fmin
        currentTasks.clear()
    return Fmin
        
def pSum(zad):
    sum = 0
    for i in range(0, len(zad)):
        sum += zad[i][0]
    return sum

def dynamicRecursionStart(zad):
    availableTasks = copy.deepcopy(zad)
    knownValues = {'0'*len(zad) : 0}
    binTasksToCheck = "1"*len(zad)

    def dynamicRecursion(zad, binChecking):
        availableTasks = copy.deepcopy(zad)
        Fmin = math.inf

        for i in range(0, len(availableTasks)):
            if binChecking not in knownValues:
                binChecking = changeTaskBinTo('0', binChecking, i, availableTasks)
                temp = availableTasks.pop(i)
                Faa = dynamicRecursion(availableTasks, binChecking)
                availableTasks.insert(i, temp) 
                binChecking = changeTaskBinTo('1', binChecking, i, availableTasks)

                sumOfP = pSum(copy.deepcopy(availableTasks))
                for j in range(0, len(availableTasks)):
                    binChecking = changeTaskBinTo('0', binChecking, j, availableTasks)
                    F = max((sumOfP - availableTasks[j][2]), 0) * availableTasks[j][1]
                    if binChecking not in knownValues:
                        temp = availableTasks.pop(j)
                        Faa = dynamicRecursion(availableTasks, binChecking)
                        availableTasks.insert(j, temp)    
                    F += knownValues[binChecking]

                    if F < Fmin:
                        Fmin = F
                    binChecking = changeTaskBinTo('1', binChecking, j, availableTasks)
                
                if Fmin < math.inf:
                    knownValues[binChecking] = Fmin
                else:
                    knownValues[binChecking] = Faa

            else:
                binChecking = changeTaskBinTo('1', binChecking, i, availableTasks)
              
        return Fmin

    def changeTaskBinTo(value, binCheck, taskIndex, taskList):
        binCheck = list(binCheck)
        binCheck[taskList[taskIndex][3]-1] = value
        binCheck = ''.join(binCheck)
        return binCheck

    Fmax = dynamicRecursion(availableTasks, binTasksToCheck)
    return Fmax

# Wczytanie listy zadan
zadania = loadData("data/data20.txt")

# Oryginal
print("- Oryginal -")
print("Kara (Fmax): ", calculate_Fmax(copy.deepcopy(zadania)))
print()

# Sort D
print("- SortD -")
start = timeit.default_timer()
zadaniaSortD = sortD(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Kara (Fmax): ", calculate_Fmax(copy.deepcopy(zadaniaSortD)))
print("Czas wykonania: {:f}\n".format(end-start))
print()

# Przeglad zupelny - permutacje
''' Bez sensu dla danych > 11
print("- BruteForce Permutacje -")
start = timeit.default_timer()
print("Kara (Fmax): ", optPermutations(copy.deepcopy(zadania)))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))
print()
'''

# Przeglad zupelny - rekurencja
''' Bez sensu dla danych > 10
print("- BruteForce Rekurencja -")
start = timeit.default_timer()
print("Kara (Fmax): ", optRecursionStart(copy.deepcopy(zadania)))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))
print()
'''

# Algorytm dynamiczny - iteracje
print("- Dynamiczny Iteracje -")
start = timeit.default_timer()
print("Kara (Fmax): ", dynamicIterations(copy.deepcopy(zadania)))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))
print()

# Algorytm dynamiczny - rekurencja
print("- Dynamiczny Rekurencja -")
start = timeit.default_timer()
print("Kara (Fmax): ", dynamicRecursionStart(copy.deepcopy(zadania)))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))
print()
