import copy
from itertools import permutations
import math
import timeit
from numpy import random
import numpy as np
import random


def loadData(path):
    plik = open(path, "r")
    linie = plik.readlines()
    n = int(linie[0].split()[0])
    m = int(linie[0].split()[1])

    zadania = []
    for i in range(1, n+1):
        linia = linie[i].split()
        maszyny = []
        for j in range(1, 2*m, 2):
            maszyny.append(int(linia[j]))
        maszyny.append(i)
        zadania.append(maszyny)
    plik.close()

    return zadania

def loadDataB(path):
    plik = open(path, "r")
    linie = plik.readlines()
    n = int(linie[1].split()[0])
    m = int(linie[1].split()[1])

    zadania = []
    for i in range(2, n+2):
        linia = linie[i].split()
        maszyny = []
        for j in range(1, 2*m, 2):
            maszyny.append(int(linia[j]))
        maszyny.append(i-1)
        zadania.append(maszyny)
    plik.close()

    return zadania

def getOrder(zad):
    kolejnosc = []
    for i in range(0, len(zad)):
        kolejnosc.append(zad[i][-1])
    return kolejnosc

def calculate_Cmax(zad):
    if len(zad) == 0:
        return math.inf

    S = []
    C = []
    Szad = []
    Czad = []

    Szad.append(0)
    Czad.append(zad[0][0])

    for i in range(0, len(zad)):
        for j in range(0, len(zad[i])-1):
            if i == 0 and j != 0:
                Szad.append(Czad[j-1])
                Czad.append(Szad[j] + zad[i][j])
            elif i != 0:
                if j == 0:
                    Szad.append(C[i-1][0])
                    Czad.append(Szad[0] + zad[i][0])
                else:
                    Szad.append(max(Czad[j-1], C[i-1][j]))
                    Czad.append(Szad[j] + zad[i][j])

        S.append(Szad.copy())
        C.append(Czad.copy())
        Szad.clear()
        Czad.clear()

    return C[-1][-1]

def calculate_C(zad):
    S = []
    C = []
    Szad = []
    Czad = []

    Szad.append(0)
    Czad.append(zad[0][0])

    for i in range(0, len(zad)):
        for j in range(0, len(zad[i])-1):
            if i == 0 and j != 0:
                Szad.append(Czad[j-1])
                Czad.append(Szad[j] + zad[i][j])
            elif i != 0:
                if j == 0:
                    Szad.append(C[i-1][0])
                    Czad.append(Szad[0] + zad[i][0])
                else:
                    Szad.append(max(Czad[j-1], C[i-1][j]))
                    Czad.append(Szad[j] + zad[i][j])

        S.append(Szad.copy())
        C.append(Czad.copy())
        Szad.clear()
        Czad.clear()

    return C

def minp(z):
    minimum = math.inf
    minimum_indeks = -1
    for i in range(0, len(z)):
        for j in range(0, len(z[i])-1):
            if z[i][j] < minimum:
                minimum = z[i][j]
                minimum_indeks = i
    return minimum_indeks

def bruteForce(zad):
    perms = list(permutations(zad,r=len(zad)))
    Cmin = math.inf
    for perm in perms:
        C = calculate_Cmax(perm)
        if C < Cmin:
            Cmin = C
    return Cmin

def Johnson(zad):
    l=1
    k=len(zad)
    posortowaneZadania = [None]*k
    indeks = -1
    while zad:
        indeks = minp(zad)
        if zad[indeks][0]<zad[indeks][1]:
            posortowaneZadania[l-1] = zad[indeks]
            l += 1
        else:
            posortowaneZadania[k-1] = zad[indeks]
            k -= 1
        zad.pop(indeks)
    return posortowaneZadania

def startBranchAndBound(zad):
    zadania = copy.deepcopy(zad)
    UB = initRandomUB(copy.deepcopy(zad), 3)
    pi = []
    pistar = []
    
    def BranchAndBound(j, zad, pi):
        nonlocal pistar
        nonlocal UB
        pi.append(j)
        zad.remove(j)
        if(len(zad) != 0):
            #LB = Bound2(copy.deepcopy(pi), copy.deepcopy(zad), copy.deepcopy(zadania))
            LB = Bound4(copy.deepcopy(pi), copy.deepcopy(zad))
            if(LB < UB):
                for j in zad:
                    BranchAndBound(j, copy.deepcopy(zad), copy.deepcopy(pi))
        else:
            Cmax = calculate_Cmax(copy.deepcopy(pi))
            if(Cmax < UB):
                UB = Cmax
                pistar = pi

    for j in zad:
        BranchAndBound(j, copy.deepcopy(zad), copy.deepcopy(pi))
    return pistar

def initRandomUB(zad, k):
    Cmin = math.inf
    for i in range(0, k):
        C = calculate_Cmax(np.random.permutation(zad))
        if C < Cmin:
            Cmin = C
    return Cmin

def Bound1(pi, zad):
    LBmax = 0
    LB = 0
    x = len(pi)-1
    C = calculate_C(copy.deepcopy(pi))
    for i in range(0, len(zad[0])-1):
        LB = C[x][i] + sumaP(copy.deepcopy(zad), i)
        if LB > LBmax:
            LBmax = LB
    return LBmax

def Bound2(pi, zad, zadania):
    LBmax = 0
    LB = 0
    x = len(pi)-1
    C = calculate_C(copy.deepcopy(pi))
    for i in range(0, len(zad[0])-1):
        LB = C[x][i] + sumaP(copy.deepcopy(zad), i) + sumaMinP(copy.deepcopy(zadania), i)
        if LB > LBmax:
            LBmax = LB
    return LBmax

def Bound3(pi, zad):
    LBmax = 0
    LB = 0
    x = len(pi)-1
    C = calculate_C(copy.deepcopy(pi))
    for i in range(0, len(zad[0])-1):
        LB = C[x][i] + sumaP(copy.deepcopy(zad), i) + sumaMinP(copy.deepcopy(zad), i)
        if LB > LBmax:
            LBmax = LB
    return LBmax

def Bound4(pi, zad):
    LBmax = 0
    LB = 0
    x = len(pi)-1
    C = calculate_C(copy.deepcopy(pi))
    for i in range(0, len(zad[0])-1):
        LB = C[x][i] + sumaP(copy.deepcopy(zad), i) + minSumaP(copy.deepcopy(zad), i)
        if LB > LBmax:
            LBmax = LB
    return LBmax

def sumaP(zad, i):
    suma = 0
    for j in zad:
        suma += j[i]
    return suma

def sumaMinP(zad, i):
    suma = 0
    m = len(zad[0])-1
    for k in range(i+1, m):
        minP = math.inf
        for j in zad:
            p = j[k]
            if p < minP:
                minP = p
        suma += minP
    return suma

def minSumaP(zad, i):
    minSuma = math.inf
    m = len(zad[0])-1
    for j in zad:
        suma = 0
        for k in range(i+1, m):
            suma += j[k]
        if minSuma > suma:
            minSuma = suma
    return minSuma

def NEH(zad):
    k = 1
    W = []
    pistar = []
    pi = []

    for zadanie in zad:
        sumaP = 0
        for i in range(0, len(zadanie)-1):
            sumaP += zadanie[i]
        W.append([sumaP, zadanie[-1]]) 
    Wsorted = sortP(W)

    while(len(W) != 0):
        idxMaxP = Wsorted[-1][1] - 1
        zadMaxP = zad[idxMaxP]
        for l in range(0, k):
            pi.insert(l, zadMaxP)
            if l == 0:
                pistar.insert(l, zadMaxP)
            if(calculate_Cmax(copy.deepcopy(pi)) < calculate_Cmax(copy.deepcopy(pistar))):
                pistar = copy.deepcopy(pi)
            pi.pop(l)

        pi = copy.deepcopy(pistar)
        Wsorted.pop()
        k += 1

    return pistar

def sortP(tabSumP):
    while True:
        zmiana = False
        for j in range(0, len(tabSumP)-1):
            if tabSumP[j][0] > tabSumP[j+1][0]:
                tabSumP[j], tabSumP[j+1] = tabSumP[j+1], tabSumP[j]
                zmiana = True

        if zmiana == False:
            return tabSumP

def NEHplus(zad):
    k = 1
    W = []
    pistar = []
    pi = []

    for zadanie in zad:
        sumaP = 0
        for i in range(0, len(zadanie)-1):
            sumaP += zadanie[i]
        W.append([sumaP, zadanie[-1]]) 
    Wsorted = sortP(W)

    while(len(W) != 0):
        idxMaxP = Wsorted[-1][1] - 1
        zadMaxP = zad[idxMaxP]
        for l in range(0, k):
            pi.insert(l, zadMaxP)
            if l == 0:
                pistar.insert(l, zadMaxP)
            if(calculate_Cmax(pi) < calculate_Cmax(pistar)):
                pistar = copy.deepcopy(pi)
            pi.pop(l)

        pi = copy.deepcopy(pistar)
        poprzednioWybrane = Wsorted.pop()

        x = selectX4(copy.deepcopy(pistar), poprzednioWybrane[1])       ###
        pi.remove(x)
        for l in range(0, k):
            pi.insert(l, x)
            if l == 0:
                pistar.insert(l, x)
            if(calculate_Cmax(pi) < calculate_Cmax(pistar)):
                pistar = copy.deepcopy(pi)
            pi.pop(l)

        pi = copy.deepcopy(pistar)
        k += 1

    return pistar

def selectX1(zad, nieToNumer):      # Zadanie zawierające najdłuższą operacje na ścieżce krytycznej.
    C = calculate_C(zad)
    pMax = C[-1][-1]
    indeksZ = len(zad)-1
    i = indeksZ
    j = len(zad[0])-2

    while i != 0 and j != 0:
        if i > 0 and j > 0:
            if C[i-1][j] >= C[i][j-1]:
                if zad[i-1][j] > pMax:
                    if zad[i-1][-1] != nieToNumer:
                        pMax = zad[i-1][j]
                        indeksZ = i-1
                i -= 1
            else:
                if zad[i][j-1] > pMax:
                    if zad[i][-1] != nieToNumer:
                        pMax = zad[i][j-1]
                        indeksZ = i
                j -= 1
        elif i == 0:
            if zad[i][j-1] > pMax:
                if zad[i][-1] != nieToNumer:
                    pMax = zad[i][j-1]
                    indeksZ = i
            j -= 1
        else:
            if zad[i-1][j] > pMax:
                if zad[i-1][-1] != nieToNumer:
                    pMax = zad[i-1][j]
                    indeksZ = i-1
            i -= 1

    return zad[indeksZ]

def selectX2(zad, nieToNumer):      # Zadanie zawierające największą sumę operacji wchodzących w ścieżkę krytyczną.
    C = calculate_C(zad)
    sumaMax = 0
    suma = C[-1][-1]

    indeksZ = len(zad)-1
    i = indeksZ
    j = len(zad[0])-2

    while i != 0 and j != 0:
        if i > 0 and j > 0:
            if C[i-1][j] >= C[i][j-1]:
                if zad[i][-1] != nieToNumer:
                    if sumaMax < suma:
                        sumaMax = suma
                        indeksZ = i
                i -= 1
                suma = 0
            else:
                suma += zad[i][j-1]
                indeksZ = i
                j -= 1
        elif i == 0:
            suma += zad[i][j-1]
            indeksZ = i
            j -= 1
        else:
            if C[i-1][j] >= C[i][j-1]:
                if zad[i][-1] != nieToNumer:
                    if sumaMax < suma:
                        sumaMax = suma
                        indeksZ = i
                i -= 1
                suma = 0

    return zad[indeksZ]

def selectX3(zad, nieToNumer):      # Zadanie zawierające największą liczbę operacji wchodzących w ścieżkę krytyczną.
    C = calculate_C(zad)
    sumaMax = 0
    suma = 1

    indeksZ = len(zad)-1
    i = indeksZ
    j = len(zad[0])-2

    while i != 0 and j != 0:
        if i > 0 and j > 0:
            if C[i-1][j] >= C[i][j-1]:
                if zad[i][-1] != nieToNumer:
                    if sumaMax < suma:
                        sumaMax = suma
                        indeksZ = i
                i -= 1
                suma = 0
            else:
                suma += 1
                indeksZ = i
                j -= 1
        elif i == 0:
            suma += 1
            indeksZ = i
            j -= 1
        else:
            if C[i-1][j] >= C[i][j-1]:
                if zad[i][-1] != nieToNumer:
                    if sumaMax < suma:
                        sumaMax = suma
                        indeksZ = i
                i -= 1
                suma = 0

    return zad[indeksZ]

def selectX4(zad, nieToNumer):          # Zadanie, którego usunięcie spowoduję największe zmniejszenie wartości Cmax.
    CmaxStart = calculate_Cmax(zad)
    index = -1

    for l in range(0, len(zad)):
        if zad[l][-1] != nieToNumer:
            usunieteZad = zad.pop(l)
            Cmax = calculate_Cmax(zad)
            zad.insert(l, usunieteZad)

            if Cmax < CmaxStart:
                CmaxStart = Cmax
                index = l
        

    return zad[index]

def algorytmSA(zad):
    pistar = []
    n = len(zad)
    T = 100                 # T0 = {100 | 1000 | 10000}
    Tend = 0.01             # Tend = {0.01 | 0.001 | 0.0001}
    pi = copy.deepcopy(zad) # pi = {neutralna | losowa | NEH}
    L = n                   # L = {sqrt(n) | n | n^2}
    x = T/10**3             # x = {T/10^3 | T/10^4 | T/10^5}
    alfa = 0.95             # alfa = {0.97 | 0.95 | 0.90}
    it = 1

    while T > Tend:
        for k in range(1, L):
            i = random.randint(0, n-1)
            j = random.randint(0, n-1)
            pinew = moveInsert(copy.deepcopy(pi), i, j)     ###

            piCmax = calculate_Cmax(pi)
            pinewCmax = calculate_Cmax(pinew)
            if pinewCmax > piCmax:
                r = random.random()
                dCmax = piCmax - pinewCmax
                if r >= math.exp(dCmax/T):
                    pinew = copy.deepcopy(pi)

            pi = copy.deepcopy(pinew)

            if calculate_Cmax(pi) < calculate_Cmax(pistar):
                pistar = copy.deepcopy(pi)
        
        #T = T - x
        #T = alfa*T
        T = T/(math.log(it+1))
        
        it += 1

    return pistar


def moveSwap(zad, i, j):
    zad[i], zad[j] = zad[j], zad[i]
    return zad

def moveInsert(zad, i, j):
    zad.insert(j, zad.pop(i))
    return zad

# _____________ MAIN _____________ #

#zadania = loadData("data/data2.txt")


print(" - - - - ta050 - - - - ")
zadania = loadDataB("dataB/ta050.txt")
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))


'''
print(" - - - - ta041 - - - - ")
zadania = loadDataB("dataB/ta041.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta042 - - - - ")
zadania = loadDataB("dataB/ta042.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta043 - - - - ")
zadania = loadDataB("dataB/ta043.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta044 - - - - ")
zadania = loadDataB("dataB/ta044.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta045 - - - - ")
zadania = loadDataB("dataB/ta045.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta046 - - - - ")
zadania = loadDataB("dataB/ta046.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta047 - - - - ")
zadania = loadDataB("dataB/ta047.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta048 - - - - ")
zadania = loadDataB("dataB/ta048.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta049 - - - - ")
zadania = loadDataB("dataB/ta049.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta050 - - - - ")
zadania = loadDataB("dataB/ta050.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n ----------------------------------------------------------------")
print("\n - - - - ta001 - - - - ")
zadania = loadDataB("dataB/ta001.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta011 - - - - ")
zadania = loadDataB("dataB/ta011.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta021 - - - - ")
zadania = loadDataB("dataB/ta021.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta031 - - - - ")
zadania = loadDataB("dataB/ta031.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta041 - - - - ")
zadania = loadDataB("dataB/ta041.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta051 - - - - ")
zadania = loadDataB("dataB/ta051.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta061 - - - - ")
zadania = loadDataB("dataB/ta061.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta071 - - - - ")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta081 - - - - ")
zadania = loadDataB("dataB/ta081.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta091 - - - - ")
zadania = loadDataB("dataB/ta091.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta101 - - - - ")
zadania = loadDataB("dataB/ta101.txt")
print(" - - - NEH - - - ")
print(calculate_Cmax(NEH(copy.deepcopy(zadania))))
print(" - - - NEH+ - - - ")
print(calculate_Cmax(NEHplus(copy.deepcopy(zadania))))
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))

print("\n - - - - ta111 - - - - ")
zadania = loadDataB("dataB/ta111.txt")
print(" - - - SAA - - - ")
print(calculate_Cmax(algorytmSA(copy.deepcopy(zadania))))
'''

''' CZESC 1: BruteForce, Johnson, BnB
# - - - DATA 1 - - - #
zadania = loadData("data/data006.txt")
print(" - - - Data001 - - - ")

print("BruteForce")
start = timeit.default_timer()
bruteForce(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))


print("Johnson")
start = timeit.default_timer()
print(calculate_Cmax(Johnson(copy.deepcopy(zadania))))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

print("BranchNBound_UB3_LB4")
start = timeit.default_timer()
startBranchAndBound(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

# - - - DATA 2 - - - #
zadania = loadData("data/data002.txt")
print(" - - - Data002 - - - ")

print("BruteForce")
start = timeit.default_timer()
bruteForce(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

print("BranchNBound_UB3_LB4")
start = timeit.default_timer()
startBranchAndBound(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

# - - - DATA 3 - - - #
zadania = loadData("data/data003.txt")
print(" - - - Data003 - - - ")

print("BruteForce")
start = timeit.default_timer()
bruteForce(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

print("Johnson")
start = timeit.default_timer()
Johnson(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

print("BranchNBound_UB3_LB4")
start = timeit.default_timer()
startBranchAndBound(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

# - - - DATA 4 - - - #
zadania = loadData("data/data004.txt")
print(" - - - Data004 - - - ")

print("BruteForce")
start = timeit.default_timer()
bruteForce(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

print("BranchNBound_UB3_LB4")
start = timeit.default_timer()
startBranchAndBound(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

Duuugo (oprocz Johnosna)
# - - - DATA 5 - - - #
zadania = loadData("data/data005.txt")
print(" - - - Data005 - - - ")

print("BruteForce")
start = timeit.default_timer()
bruteForce(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

print("Johnson")
start = timeit.default_timer()
Johnson(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

print("BranchNBound_UB3_LB4")
start = timeit.default_timer()
startBranchAndBound(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

# - - - DATA 6 - - - #
zadania = loadData("data/data006.txt")
print(" - - - Data006 - - - ")

print("BruteForce")
start = timeit.default_timer()
bruteForce(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))

print("BranchNBound_UB3_LB4")
start = timeit.default_timer()
startBranchAndBound(copy.deepcopy(zadania))
end = timeit.default_timer()
print("Czas wykonania: {:f}\n".format(end-start))
'''