
def rozparsuj_linie(line):
    czesci = line.split(";")
    wagi = list(map(int, czesci[0].strip("[]").split()))
    wartosci = list(map(int, czesci[1].strip("[]").split()))
    maks_pojemnosc = int(czesci[2])
    return (wagi, wartosci, maks_pojemnosc)
            