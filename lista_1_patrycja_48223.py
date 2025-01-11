import numpy as np

def rozparsuj_linie(line):
    czesci = line.split(";")
    wagi = np.array(list(map(int, czesci[0].strip("[]").split())))
    wartosci = np.array(list(map(int, czesci[1].strip("[]").split())))
    maks_pojemnosc = int(czesci[2])
    return (wagi, wartosci, maks_pojemnosc)
            
def generuj_poczatkowa_populacje(rozmiar_populacji, liczba_przedmiotow):
    populacja = np.random.choice([True, False], size=(rozmiar_populacji, liczba_przedmiotow))
    return populacja

def funkcja_dostosowania(populacja, wartosci, wagi, maks_pojemnosc):
    suma_wag = np.dot(populacja, wagi)
    suma_wartosci = np.dot(populacja, wartosci)

    dostosowanie = np.where(suma_wag > maks_pojemnosc, 0, suma_wartosci)
    return dostosowanie

def main():
    with open("zbior_danych_ag.csv") as csv_file:
        for i, linia in enumerate(list(csv_file)):
            if i == 0:
                continue
            wagi, wartosci, maks_pojemnosc = rozparsuj_linie(linia)
            print(f" Przypadek {linia}")
            rozmiar_populacji = 20
            liczba_przedmiotow = len(wartosci)
            populacja = generuj_poczatkowa_populacje(rozmiar_populacji, liczba_przedmiotow)
            print("  Populacja początkowa:")
            for chromosom in populacja:
                print(chromosom)

            print("\n  Dostosowanie chromosomów:")
            wyniki_dostosowania = funkcja_dostosowania(populacja, wartosci, wagi, maks_pojemnosc)
            for chromosom, wynik in zip(populacja, wyniki_dostosowania):
                print(f"  Chromosom: {chromosom}, Dostosowanie: {wynik}")

if __name__ == "__main__":
    main()
