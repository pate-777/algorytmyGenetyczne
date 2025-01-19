import time
from algorytm_genetyczny import mutacja_punktowa
from utils import rozparsuj_linie

DATA_FILE="zbior_danych_ag_2.csv"


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

def zmierz_roznorodnosc_populacji(populacja):
    unikalne_chromosomy = set(tuple(chromosom) for chromosom in populacja)
    return len(unikalne_chromosomy) / len(populacja)

def test_mutacji(populacja, prawdopodobienstwo_mutacji, liczba_iteracji):
    roznorodnosc_na_iteracje = []
    for _ in range(liczba_iteracji):
        populacja = [mutacja_punktowa(chromosom, prawdopodobienstwo_mutacji) for chromosom in populacja]
        roznorodnosc = zmierz_roznorodnosc_populacji(populacja)
        roznorodnosc_na_iteracje.append(roznorodnosc)
    return roznorodnosc_na_iteracje


def main():
    with open(DATA_FILE) as csv_file:
        for i, linia in enumerate(list(csv_file)):
            if i == 0:
                continue
            wagi, wartosci, maks_pojemnosc = rozparsuj_linie(linia)
            print(f" Przypadek {linia}")

if __name__ == "__main__":
    main()