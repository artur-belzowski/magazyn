import json
import os

if not os.path.exists('firma.json):
    firma = {
        'stan_konta':0,
        'stan_magazynu':{},
        'historia': []
}
while True:

    with open('firma.json', 'w') as f:
        json.dump(firma, f)

    print("Dostępne komendy: saldo, sprzedaż, zakup, konto, lista, magazyn, przegląd, koniec")
    komenda = input("Podaj komendę: ")

    if komenda == "saldo":

        operacja = input("Czy chcesz dodać (+) czy odjąć (-) kwotę? ")
        kwota = float(input("Podaj kwotę: "))
        if operacja == "+":
            firma['stan_konta'] += kwota
            print(f"Dodano {kwota} zł do stanu konta.")
            firma['historia'].append([firma['stan_konta'], kwota])
        elif operacja == "-":
            firma['stan_konta'] -= kwota
            print(f"Odjęto {kwota} zł od stanu konta.")
            firma['historia'].append([firma['stan_konta'], kwota])
        else:
            print("Nieznana operacja, spróbuj ponownie.")

    elif komenda == "sprzedaż":
        nazwa_produktu = input("Podaj nazwę produktu: ")

        if nazwa_produktu in firma['stan_magazynu']:

            cena = float(input("Podaj cenę: "))

            ilosc = float(input("Podaj ilość sztuk: "))

            if ilosc <= firma['stan_magazynu'][nazwa_produktu]["ilosc"]:

                firma['stan_konta'] += ilosc * cena

                firma['stan_magazynu'][nazwa_produktu]["ilosc"] -= ilosc

                print(f"Sprzedano {ilosc} sztuk produktu {nazwa_produktu} za {ilosc * cena} zł.")

                firma['historia'].append(["sprzedaz", nazwa_produktu, ilosc, cena])

            else:

                print("Nie można sprzedać tylu sztuk. Nie ma wystarczającej ilości produktu na magazynie.")

        else:

            print("Produkt nie jest dostępny na magazynie.")

    elif komenda == "zakup":

        nazwa_produktu = input(str("Podaj nazwę produktu: "))

        cena = float(input("Podaj cenę produktu: "))

        ilosc = float(input("Podaj ilość sztuk: "))

        # Dodaj produkt do magazynu lub zwiększ jego ilość

        if nazwa_produktu in firma['stan_magazynu']:

            firma['stan_magazynu'][nazwa_produktu]['ilosc'] += ilosc

        else:

            firma['stan_magazynu'][nazwa_produktu] = {'ilosc': ilosc}

        # Oblicz koszt zakupu i zaktualizuj stan konta

        koszt = cena * ilosc

        if firma['stan_konta'] - koszt < 0:

            print("Nie można dokonać zakupu - brak wystarczających środków na koncie.")

        else:

            firma['stan_konta'] -= koszt

            print(f"Zakupiono {ilosc} sztuk produktu {nazwa_produktu} za {koszt} zł. Stan konta: {firma['stan_konta']} zł.")
            firma['historia'].append(['zakup', nazwa_produktu, ilosc, cena])

    elif komenda == "konto":
        print(f"Stan konta obecnie to {firma['stan_konta']} PLN")

    elif komenda == "lista":
        print("Magazyn:")
        for nazwa_produktu in firma['stan_magazynu']:
            print(f"{nazwa_produktu}  ilość: {firma['stan_magazynu'][nazwa_produktu][ilosc]}")

    if komenda == 'przeglad':
        start = input('Podaj "od": ').strip()
        koniec = input('Podaj "do": ').strip()

        if start:
            start = int(start)
        if koniec:
            koniec = int(koniec)

        print(f'Wyswietlam historie od {start} do {koniec}:')
        for wpis in firma['historia'][start:koniec]:
            print(wpis)

    elif komenda == "koniec":
        break

    else:
        print("Nieznana komenda, spróbuj ponownie.")
