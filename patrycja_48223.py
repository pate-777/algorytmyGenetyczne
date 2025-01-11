import random
import time
import datetime
import pprint

DATA_FILE="zbior_danych_ag_2.csv"

def rozparsuj_linie(line):
    czesci = line.split(";")
    wagi = list(map(int, czesci[0].strip("[]").split()))
    wartosci = list(map(int, czesci[1].strip("[]").split()))
    maks_pojemnosc = int(czesci[2])
    return (wagi, wartosci, maks_pojemnosc)
            
def generuj_poczatkowa_populacje(rozmiar_populacji, liczba_przedmiotow):
    populacja = []
    for _ in range(rozmiar_populacji): 
        chromosom = []
        for _ in range(liczba_przedmiotow):
            chromosom.append(random.choice([0, 1]))
        populacja.append(chromosom)
    return populacja

def krzyzowanie_a(chromosom1, chromosom2):
    if len(chromosom1) != len(chromosom2):
        raise ValueError("Chromosomy muszą mieć taką samą długość")
    dlugosc = len(chromosom1)
    punkt_podzialu = dlugosc // 2
    return chromosom1[:punkt_podzialu] + chromosom2[punkt_podzialu:]

def krzyzowanie_b(chromosom1, chromosom2):
    if len(chromosom1) != len(chromosom2):
        raise ValueError("Chromosomy muszą mieć taką samą długość")
    potomstwo = []
    pprint.pprint(list(zip(chromosom1, chromosom2)))
    for gen1, gen2 in zip(chromosom1, chromosom2):
        potomstwo.append(random.choice([gen1, gen2]))
    return potomstwo

def funkcja_dostosowania(chromosom, wartosci, wagi, maks_pojemnosc):
    suma_wartosci = 0
    suma_wag = 0
    
    for i in range(len(chromosom)):
        if chromosom[i] == 1:
            suma_wartosci += wartosci[i]
            suma_wag += wagi[i]
    
    if suma_wag > maks_pojemnosc:
        return 0
    return suma_wartosci

def selekcja_turniejowa(populacja, wyniki_dostosowania_dict, rozmiar_turnieju):
    zwyciezcy = []
    for _ in range(len(populacja)):
        uczestnicy = random.sample(list(populacja), rozmiar_turnieju)
        najlepszy_uczestnik = uczestnicy[0]
        najlepsze_dostosowanie = wyniki_dostosowania_dict[tuple(najlepszy_uczestnik)]
        for uczestnik in uczestnicy[1:]:
            dostosowanie = wyniki_dostosowania_dict[tuple(uczestnik)]
            if dostosowanie > najlepsze_dostosowanie:
                najlepszy_uczestnik = uczestnik
                najlepsze_dostosowanie = dostosowanie
        zwyciezcy.append(najlepszy_uczestnik)
    return zwyciezcy

def selekcja_ruletki(populacja, wyniki_dostosowania_dict):
    suma_dostosowania = sum(wyniki_dostosowania_dict.values())
    wybrane = []
    for _ in range(len(populacja)):
        prog = random.uniform(0, suma_dostosowania)
        akumulacja = 0
        for chromosom in populacja:
            akumulacja += wyniki_dostosowania_dict[tuple(chromosom)]
            if akumulacja >= prog:
                wybrane.append(chromosom)
                break
    return wybrane

def mutacja_punktowa(chromosom, prawdopodobienstwo_mutacji):
    for i in range(len(chromosom)):
        if random.random() < prawdopodobienstwo_mutacji:
            chromosom[i] = 1 - chromosom[i]  # Zamiana 0 na 1 lub 1 na 0
    return chromosom

def test_selekcji(populacja, wyniki_dostosowania_dict, metoda_selekcji, *args):
    start_time = time.time_ns()
    wybrana_populacja = metoda_selekcji(populacja, wyniki_dostosowania_dict, *args)
    end_time = time.time_ns()
    czas_wykonania = end_time - start_time
    suma_dostosowania = sum(wyniki_dostosowania_dict[tuple(chromosom)] for chromosom in wybrana_populacja)
    return suma_dostosowania, czas_wykonania

def test_krzyzowania(chromosom1, chromosom2, funkcja_krzyzowania):
    potomstwo = funkcja_krzyzowania(chromosom1, chromosom2)
    assert len(potomstwo) == len(chromosom1), "Długość potomstwa nie jest zgodna z długością rodziców"
    for gen in potomstwo:
        assert gen in [0, 1], "Gen potomstwa nie jest binarny"
    print(f" chromosom1: {chromosom1}, chromosom2: {chromosom2}, potomostwo: {potomstwo}")
    print(f"Test krzyżowania {funkcja_krzyzowania.__name__} zakończony sukcesem")

def main():
    with open(DATA_FILE) as csv_file:
        for i, linia in enumerate(list(csv_file)):
            if i == 0:
                continue
            wagi, wartosci, maks_pojemnosc = rozparsuj_linie(linia)
            print(f" Przypadek {linia}")
            rozmiar_populacji = 15
            liczba_przedmiotow = len(wartosci)
            populacja = generuj_poczatkowa_populacje(rozmiar_populacji, liczba_przedmiotow)
            wyniki_dostosowania_dict = {tuple(chromosom): funkcja_dostosowania(chromosom, wartosci, wagi, maks_pojemnosc) for chromosom in populacja}

            print("\n  Test selekcji turniejowej:")
            suma_dostosowania_turniej, czas_turniej = test_selekcji(populacja, wyniki_dostosowania_dict, selekcja_turniejowa, 3)
            print(f"  Suma dostosowania: {suma_dostosowania_turniej}, Czas wykonania: {czas_turniej} ns")

            print("\n  Test selekcji ruletki:")
            suma_dostosowania_ruletka, czas_ruletka = test_selekcji(populacja, wyniki_dostosowania_dict, selekcja_ruletki)
            print(f"  Suma dostosowania: {suma_dostosowania_ruletka}, Czas wykonania: {czas_ruletka} ns")

            # Testy krzyżowania
            # chromosom1 = populacja[0]
            # chromosom2 = populacja[1]
            chromosom1 = [1, 0 ,1, 0, 1]
            chromosom2 = [0, 1 ,0, 1, 1]
            print("\n  Testy krzyżowania:")
            test_krzyzowania(chromosom1, chromosom2, krzyzowanie_a)
            # test_krzyzowania(chromosom1, chromosom2, krzyzowanie_b)

if __name__ == "__main__":
    main()
