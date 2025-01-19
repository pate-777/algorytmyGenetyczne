import random
import pprint
from typing import Callable, Dict, List, Tuple

class WynikPokolenia:
    def __init__(self, najlepszy: int, najgorszy: int, sredni: float) -> None:
        self.najlepszy = najlepszy
        self.najgorszy = najgorszy
        self.sredni = sredni

    def __repr__(self) -> str:
        return f"WynikPokolenia(najlepszy={self.najlepszy}, najgorszy={self.najgorszy}, sredni={self.sredni})"

def krzyzowanie_jednopunktowe(populacja: List[List[int]]) -> List[List[int]]: 
    nowa_populacja = []
    for i in range(0, len(populacja), 2):
        chromosom1 = populacja[i]
        chromosom2 = populacja[i + 1]
        if len(chromosom1) != len(chromosom2):
            raise ValueError("Chromosomy muszą mieć taką samą długość")
        dlugosc = len(chromosom1)
        punkt_podzialu = dlugosc // 2
        dziecko1 = chromosom1[:punkt_podzialu] + chromosom2[punkt_podzialu:]
        dziecko2 = chromosom2[:punkt_podzialu] + chromosom1[punkt_podzialu:]
        nowa_populacja.extend([dziecko1, dziecko2])
    return nowa_populacja

def krzyzowanie_jednorodne(populacja: List[List[int]]) -> List[List[int]]:
    nowa_populacja = []
    for i in range(0, len(populacja), 2):
        chromosom1 = populacja[i]
        chromosom2 = populacja[i + 1]
        if len(chromosom1) != len(chromosom2):
            raise ValueError("Chromosomy muszą mieć taką samą długość")
        dziecko1 = []
        dziecko2 = []
        for gen1, gen2 in zip(chromosom1, chromosom2):
            dziecko1.append(random.choice([gen1, gen2]))
            dziecko2.append(random.choice([gen1, gen2]))
        nowa_populacja.extend([dziecko1, dziecko2])
    return nowa_populacja

def selekcja_turniejowa(populacja: List[List[int]],
                       wyniki_dostosowania_dict: Dict[Tuple[int], int],
                       rozmiar_turnieju: int) -> List[List[int]]:
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

def selekcja_ruletki(populacja: List[List[int]], wyniki_dostosowania_dict: Dict[Tuple[int], int]) -> List[List[int]]:
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

def mutacja_punktowa(populacja: List[List[int]], prawdopodobienstwo_mutacji: float) -> List[List[int]]:
    nowa_populacja = []
    for chromosom in populacja:
        nowy_chromosom = chromosom[:]
        for i in range(len(nowy_chromosom)):
            if random.random() < prawdopodobienstwo_mutacji:
                nowy_chromosom[i] = 1 - nowy_chromosom[i]  # Zamiana 0 na 1 i odwrotnie
        nowa_populacja.append(nowy_chromosom)
    return nowa_populacja

class AlgorytmGenetyczny:
    def __init__(self,
                  rozmiar_populacji: int,
                  liczba_przedmiotow: int,
                  wagi: List[int],
                  wartosci: List[int],
                  maks_pojemnosc: int,
                  krzyzowanie: Callable[[List[int], List[int]], List[int]],
                  selekcja: Callable[[List[List[int]], Dict[Tuple[int], int]], List[List[int]]],
                  mutacja: Callable[[List[List[int]], float], List[int]],
                  prawdopodobienstwo_mutacji: float = 0.01) -> None:
        self.populacja = self.generuj_poczatkowa_populacje(rozmiar_populacji, liczba_przedmiotow)
        self.wagi = wagi
        self.wartosci = wartosci
        self.maks_pojemnosc = maks_pojemnosc
        self.krzyzowanie = krzyzowanie
        self.selekcja = selekcja
        self.mutacja = mutacja
        self.wyniki_dostosowania_dict = {tuple(chromosom): self.funkcja_dostosowania(chromosom, wartosci, wagi, maks_pojemnosc) for chromosom in self.populacja}
        self.prawdopodobienstwo_mutacji = prawdopodobienstwo_mutacji

    def generuj_poczatkowa_populacje(self,rozmiar_populacji: int, liczba_przedmiotow: int) -> List[List[int]]:
        populacja = []
        for _ in range(rozmiar_populacji): 
            chromosom = []
            for _ in range(liczba_przedmiotow):
                chromosom.append(random.choice([0, 1]))
            populacja.append(chromosom)
        return populacja


    def funkcja_dostosowania(self, chromosom: List[int],
                            wartosci: List[int],
                            wagi: List[int],
                            maks_pojemnosc: int) -> int:
        suma_wartosci = 0
        suma_wag = 0
        for i in range(len(chromosom)):
            if chromosom[i] == 1:
                suma_wartosci += wartosci[i]
                suma_wag += wagi[i]
        if suma_wag > maks_pojemnosc:
            return 0
        return suma_wartosci

    def przeprowadz_algorytm(self, liczba_generacji: int) -> Tuple[List[int], List[WynikPokolenia]]:
        wyniki_pokolen = []
        for _ in range(1, liczba_generacji + 1):
            populacja_selekcja = self.selekcja(self.populacja, self.wyniki_dostosowania_dict)
            populacja_krzyzowanie = self.krzyzowanie(populacja_selekcja)
            populacja_mutacja = self.mutacja(populacja_krzyzowanie, self.prawdopodobienstwo_mutacji)
            nowa_populacja = populacja_mutacja
            
            self.wyniki_dostosowania_dict = {tuple(chromosom): self.funkcja_dostosowania(chromosom, self.wartosci, self.wagi, self.maks_pojemnosc) for chromosom in nowa_populacja}
            self.populacja = nowa_populacja
            
            najlepszy_chromosom = max(self.populacja, key=lambda chromosom: self.wyniki_dostosowania_dict[tuple(chromosom)])
            najgorszy_chromosom = min(self.populacja, key=lambda chromosom: self.wyniki_dostosowania_dict[tuple(chromosom)])
            srednia_wartosc = sum(self.wyniki_dostosowania_dict[tuple(chromosom)] for chromosom in self.populacja) / len(self.populacja)
            
            wynik_pokolenia = WynikPokolenia(
                najlepszy=self.wyniki_dostosowania_dict[tuple(najlepszy_chromosom)],
                najgorszy=self.wyniki_dostosowania_dict[tuple(najgorszy_chromosom)],
                sredni=srednia_wartosc
            )
            wyniki_pokolen.append(wynik_pokolenia)
        
        return najlepszy_chromosom, wyniki_pokolen