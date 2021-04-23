import copy
from itertools import permutations
import math
import timeit
from numpy import random
import numpy as np
import random


def zaladujDane(path):
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

def IA(zad):
    wyspy = []
    populacja = []
    iloscWysp = 5
    wielkoscPopulacji = 20
    liczbaEpok = 100

    for i in range(0, iloscWysp):
        print("Nowa wyspa nr ", i+1)
        for j in range(0, wielkoscPopulacji-1):
            populacja.append(np.random.permutation(zad))
        populacja.append(NEH(copy.deepcopy(zad)))
        wyspy.append(copy.deepcopy(populacja))
        populacja.clear()

    print("Pomiedzy")
    for i in range(0, liczbaEpok):
        print("-> Epoka nr ", i+1)
        akcjaNaWyspie(wyspy)
        if not i % 4:
            print("Migracja")
            migracjeNaWyspy(wyspy)

    return znajdzNajlepszegoOsobnika(wyspy)

def akcjaNaWyspie(wyspy):
    print("Krzyzowanie")
    wyspy = krzyzowanie(wyspy)
    print("Mutacje")
    mutacje(wyspy)

def krzyzowanie(wyspy):
    nowaPopulacja = []

    for wyspa in wyspy:
        for indeks in range(0, len(wyspa)):
            nowaPopulacja.append(krzyzujOsobniki(wyspa[indeks-1], wyspa[indeks]))
        
        wyspa = sortCmax(wyspa)
        nowaPopulacja = sortCmax(nowaPopulacja)
        for i in range(len(wyspa)//5, len(wyspa)):
            wyspa[i] = nowaPopulacja[i-len(wyspa)//5]

        nowaPopulacja.clear()

    return wyspy

def sortCmax(wyspa):
    while True:
        zmiana = False
        for j in range(0, len(wyspa)-1):
            if calculate_Cmax(wyspa[j]) > calculate_Cmax(wyspa[j+1]):
                wyspa[j], wyspa[j+1] = wyspa[j+1], wyspa[j]
                zmiana = True

        if zmiana == False:
            return wyspa

def krzyzujOsobniki(osobnik1, osobnik2):
    nowyOsobnik = [None] * len(osobnik1)
    punkt1 = len(osobnik1)//4
    punkt2 = (len(osobnik1)//4)*3

    for i in range(punkt1, punkt2):
        nowyOsobnik[i] = copy.deepcopy(osobnik1[i])

    indeks = 0
    for i in range(0, len(osobnik2)):
        czyWystepujeGen = False
        for j in range(punkt1, punkt2):
            if osobnik2[i][-1] == osobnik1[j][-1]:
                czyWystepujeGen = True
        if czyWystepujeGen == False:
            nowyOsobnik[indeks] = copy.deepcopy(osobnik2[i])
            indeks += 1
            if indeks == len(osobnik2):
                return nowyOsobnik
            if indeks == punkt1:
                indeks = punkt2

    return nowyOsobnik

def mutacje(wyspy):
    procentMutacji = 0.03
    for wyspa in wyspy:
        for indeks in range(0, len(wyspa)):
            prawdopodobienstwoMutacji = random.random()
            if prawdopodobienstwoMutacji <= procentMutacji:
                gen1 = random.randint(0, len(wyspa[0])-1)
                gen2 = random.randint(0, len(wyspa[0])-1)
                moveSwap(wyspa[indeks], gen1, gen2)

def moveSwap(osobnik, i, j):
    #print("Przed mutacja: ", osobnik)
    temp = copy.deepcopy(osobnik[i])
    osobnik[i] = copy.deepcopy(osobnik[j])
    osobnik[j] = copy.deepcopy(temp)
    #osobnik[i], osobnik[j] = osobnik[j], osobnik[i]
    #print("Po mutacji: ", osobnik)

def migracjeNaWyspy(wyspy):
    iloscEmigrantow = 2

    for indeks, wyspa in enumerate(wyspy):
        for i in range(0, iloscEmigrantow):
            numerOsobnika = random.randint(0, len(wyspa)-1)
            moveSwapPomiedzyWyspami(wyspy[indeks], wyspy[indeks-1], numerOsobnika)
            numerOsobnika = random.randint(0, len(wyspa)-1)
            if indeks >= len(wyspy)-1:
                moveSwapPomiedzyWyspami(wyspy[indeks], wyspy[0], numerOsobnika)
            else:
                moveSwapPomiedzyWyspami(wyspy[indeks], wyspy[indeks+1], numerOsobnika)

def moveSwapPomiedzyWyspami(wyspa1, wyspa2, numerOsobnika):
    wyspa1[numerOsobnika], wyspa2[numerOsobnika] = wyspa2[numerOsobnika], wyspa1[numerOsobnika]

def znajdzNajlepszegoOsobnika(wyspy):
    Cmin = math.inf
    najlepszyOsobnik = None

    for wyspa in wyspy:
        for osobnik in wyspa:
            C = calculate_Cmax(osobnik)
            if C < Cmin:
                Cmin = C
                najlepszyOsobnik = osobnik
    
    return najlepszyOsobnik


# - - - MAIN - - - #

zadania = zaladujDane("dataB/ta011.txt")
#print(calculate_Cmax(copy.deepcopy(zadania)))
print(calculate_Cmax(IA(zadania)))