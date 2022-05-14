historia_operacji = []
magazyn = {}

file_path = "in.txt"


# wczytywanie danych z zewnętrznego pliku z historią operacji i zapisanie ich do historii operacji wewnątrz programu
def dotychczasowa_historia_operacji():
    with open(file_path, 'r') as f:
        while True:
            dana_z_wejscia = f.readline().strip()
            if dana_z_wejscia == "saldo":
                zmiana_na_koncie = f.readline().strip()
                nazwa_operacji = f.readline().strip()
                obecna_lista = (dana_z_wejscia, zmiana_na_koncie, nazwa_operacji)
                historia_operacji.append(obecna_lista)
            elif dana_z_wejscia == "zakup":
                nazwa_zakup = f.readline().strip()
                cena_szt_zakup = f.readline().strip()
                ilosc_zakup = f.readline().strip()
                obecna_lista = (dana_z_wejscia, nazwa_zakup, cena_szt_zakup, ilosc_zakup)
                historia_operacji.append(obecna_lista)
            elif dana_z_wejscia == "sprzedaz":
                nazwa_sprzedaz = f.readline().strip()
                cena_szt_sprzedaz = f.readline().strip()
                ilosc_sprzedaz = f.readline().strip()
                obecna_lista = (dana_z_wejscia, nazwa_sprzedaz, cena_szt_sprzedaz, ilosc_sprzedaz)
                historia_operacji.append(obecna_lista)
            elif dana_z_wejscia == "stop":
                break
            else:
                print("Błąd")
                break
    return historia_operacji


# przerobienie historii operacji na działania
def historia_na_dzialania():
    saldo = 0
    for polecenie in historia_operacji:
        if polecenie[0] == "saldo":
            kwota = polecenie[1]
            saldo += int(kwota)
            if saldo < 0:
                print("Brak wystarczających środków na koncie do przeprowadzenia operacji")
                # saldo -= kwota
                break
        elif polecenie[0] == "zakup":
            kwota = int(polecenie[2]) * int(polecenie[3])
            saldo -= kwota
            if saldo < 0 or int(polecenie[2]) < 0 or int(polecenie[3]) < 0:
                # saldo += kwota
                print("Błąd")
                break
            przedmiot = polecenie[1]
            if not magazyn.get(przedmiot):
                magazyn[przedmiot] = 0
            magazyn[przedmiot] += int(polecenie[3])
        elif polecenie[0] == "sprzedaz":
            kwota = int(polecenie[2]) * int(polecenie[3])
            saldo += kwota
            # if len(sys.argv) > 2:
            #     if not magazyn.get(sys.argv[2]):
            #         magazyn[sys.argv[2]] = 0
            liczba_sztuk_w_magazynie = int(magazyn[polecenie[1]])
            if liczba_sztuk_w_magazynie < int(polecenie[3]) or int(polecenie[2]) < 0 or int(polecenie[3]) < 0:
                # saldo -= kwota
                return "Błąd"
            magazyn[polecenie[1]] -= int(polecenie[3])
        else:
            break
    return saldo, magazyn


# dotychczasowa_historia_operacji()
# print(historia_operacji)
