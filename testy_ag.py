import time
from algorytm_genetyczny import AlgorytmGenetyczny, krzyzowanie_jednopunktowe, selekcja_turniejowa, selekcja_ruletkowa, selekcja_rankingowa, mutacja_punktowa
from utils import rozparsuj_linie

DATA_FILE = "zbior_danych_ag_2.csv"


def badanie_wplywu_rozmiaru_populacji(wagi, wartosci, maks_pojemnosc, liczba_generacji, minimalna_wartosc_dostosowania):
    rozmiary_populacji = [2, 6, 10, 50, 200]
    wyniki = {}

    for rozmiar in rozmiary_populacji:
        algorytm = AlgorytmGenetyczny(
            rozmiar_populacji=rozmiar,
            liczba_przedmiotow=len(wagi),
            wagi=wagi,
            wartosci=wartosci,
            maks_pojemnosc=maks_pojemnosc,
            krzyzowanie=krzyzowanie_jednopunktowe,
            selekcja=selekcja_turniejowa,
            mutacja=mutacja_punktowa,
            prawdopodobienstwo_mutacji=0.01
        )
        
        start_time = time.time()
        najlepszy_chromosom, wyniki_pokolen = algorytm.przeprowadz_algorytm(liczba_generacji, minimalna_wartosc_dostosowania)
        end_time = time.time()
        
        czas_wykonania = end_time - start_time
        wyniki[rozmiar] = {
            "najlepszy_chromosom": najlepszy_chromosom,
            "wyniki_pokolen": wyniki_pokolen,
            "czas_wykonania": czas_wykonania
        }
    
    return wyniki

def porownanie_metod_selekcji(wagi, wartosci, maks_pojemnosc, liczba_generacji, minimalna_wartosc_dostosowania):
    selekcje = {
        "selekcja_turniejowa": selekcja_turniejowa,
        "selekcja_ruletkowa": selekcja_ruletkowa,
        "selekcja_rankingowa": selekcja_rankingowa
    }
    wyniki = {}

    for nazwa_selekcji, metoda_selekcji in selekcje.items():
        algorytm = AlgorytmGenetyczny(
            rozmiar_populacji=50,  # Example population size
            liczba_przedmiotow=len(wagi),
            wagi=wagi,
            wartosci=wartosci,
            maks_pojemnosc=maks_pojemnosc,
            krzyzowanie=krzyzowanie_jednopunktowe,
            selekcja=metoda_selekcji,
            mutacja=mutacja_punktowa,
            prawdopodobienstwo_mutacji=0.01
        )
        
        start_time = time.time()
        najlepszy_chromosom, wyniki_pokolen = algorytm.przeprowadz_algorytm(liczba_generacji, minimalna_wartosc_dostosowania)
        end_time = time.time()
        
        czas_wykonania = end_time - start_time
        wyniki[nazwa_selekcji] = {
            "najlepszy_chromosom": najlepszy_chromosom,
            "wyniki_pokolen": wyniki_pokolen,
            "czas_wykonania": czas_wykonania
        }
    
    return wyniki

def main():
    with open(DATA_FILE) as csv_file:
        for i, linia in enumerate(list(csv_file)):
            if i == 0:
                continue
            wagi, wartosci, maks_pojemnosc = rozparsuj_linie(linia)
            print(f"Przypadek {i}: {linia.strip()}")
            
            liczba_generacji = 100
            minimalna_wartosc_dostosowania = 100  # Example value, adjust as needed
            
            wyniki = badanie_wplywu_rozmiaru_populacji(wagi, wartosci, maks_pojemnosc, liczba_generacji, minimalna_wartosc_dostosowania)
            
            for rozmiar, wynik in wyniki.items():
                print(f"Rozmiar populacji: {rozmiar}")
                print(f"Najlepszy chromosom: {wynik['najlepszy_chromosom']}")
                print(f"Czas wykonania: {wynik['czas_wykonania']}s")
                for generacja, wynik_pokolenia in enumerate(wynik['wyniki_pokolen'], start=1):
                    print(f"Generacja {generacja}: {wynik_pokolenia}")
            
            wyniki_selekcji = porownanie_metod_selekcji(wagi, wartosci, maks_pojemnosc, liczba_generacji, minimalna_wartosc_dostosowania)
            
            for nazwa_selekcji, wynik in wyniki_selekcji.items():
                print(f"Metoda selekcji: {nazwa_selekcji}")
                print(f"Najlepszy chromosom: {wynik['najlepszy_chromosom']}")
                print(f"Czas wykonania: {wynik['czas_wykonania']}s")
                for generacja, wynik_pokolenia in enumerate(wynik['wyniki_pokolen'], start=1):
                    print(f"Generacja {generacja}: {wynik_pokolenia}")

if __name__ == "__main__":
    main()