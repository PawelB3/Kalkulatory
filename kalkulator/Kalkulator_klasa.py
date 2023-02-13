import pandas as pd
import requests
import math
from parametry import *
from tabulate import tabulate
import numpy as np


class Kalkulator:

    laczne_odsetki = 0
    ostatnia_zmiana = 0

    def __init__(self,
                 kwota_kredytu: int,
                 okres_splat: OkresSplaty = OkresSplaty.raty_miesieczne,
                 ilosc_rat: int = 120,
                 rodzaj_oprocentowania: RodzajOprocentowania = RodzajOprocentowania.zmienne,
                 stopa_procentowa: float = 8,
                 rodzaj_rat: RodzajRat = RodzajRat.laczne,
                 r_kapitalizacji: RodzajKapitalizacji = RodzajKapitalizacji.ciagla,
                 okres_kapitalizacji: OkresyKapitalizacji = OkresyKapitalizacji.miesieczna):
        self.kapital = kwota_kredytu
        if ilosc_rat / okres_splat.value <= 35:
            self.ilosc_rat = ilosc_rat
        else:
            raise Exception('Kredyt może trwać maksymalnie 35 lat!')
        self.okres_splat = okres_splat
        self.rodzaj_oprocentowania = rodzaj_oprocentowania
        self.stopa_procentowa = stopa_procentowa
        self.rodzaj_rat = rodzaj_rat
        self.r_kapitalizacji = r_kapitalizacji
        self.okres_kapitalizacji = okres_kapitalizacji
        self.m = okres_kapitalizacji.value
        self.k = okres_splat.value
        if rodzaj_oprocentowania == RodzajOprocentowania.stale:
            self.r = stopa_procentowa / 100
        elif rodzaj_oprocentowania == RodzajOprocentowania.zmienne:
            self.sprawdz_stopy_referencyjne()
        else:
            raise Exception('Nieznany rodzaj oprocentowania')

        self.columns = ['Numer raty', 'Kapitał na początku okresu', 'Rata kapitałowa', 'Rata odsetkowa', 'Rata łączna',
                        'Kapitał na koniec okresu']
        self.tabela_splat = pd.DataFrame(
            columns=self.columns)

        if self.r_kapitalizacji == RodzajKapitalizacji.ciagla:
            self.kapitalizacja = math.exp((self.r / self.k))
            self.rata_laczna = round(
                (self.kapital * math.exp(self.r / self.k * self.ilosc_rat) * (math.exp(self.r / self.k) - 1) /
                 (math.exp(self.r / self.k * self.ilosc_rat) - 1)), 2)
        elif self.r_kapitalizacji == RodzajKapitalizacji.okresowa:
            self.kapitalizacja = (1 + self.r / self.m) ** (self.m / self.k)
            self.rata_laczna = round((self.kapital * self.r /
                                      (self.k * (1 - (self.k / (self.k + self.r)) ** self.ilosc_rat))), 2)
        else:
            raise Exception('Nieznany rodzaj kapitalizacji')
        self.rata_kapitalowa = round(self.kapital / self.ilosc_rat, 2)

    def oblicz_kapitalizacje(self):
        r = self.r
        k = self.k
        m = self.m
        if self.r_kapitalizacji == RodzajKapitalizacji.ciagla:
            self.kapitalizacja = math.exp((r / k))
        elif self.r_kapitalizacji == RodzajKapitalizacji.okresowa:
            self.kapitalizacja = (1 + r / m) ** (m / k)
        else:
            raise Exception('Nieznany rodzaj kapitalizacji')

    def oblicz_laczna_rate(self):
        r = self.r
        n = self.ilosc_rat
        k = self.k
        self.rata_kapitalowa = round(self.kapital / n, 2)
        if self.r_kapitalizacji == RodzajKapitalizacji.ciagla:
            self.rata_laczna = round(
                (self.kapital * math.exp(r / k * n) * (math.exp(r / k) - 1) / (math.exp(r / k * n) - 1)), 2)
        elif self.r_kapitalizacji == RodzajKapitalizacji.okresowa:
            self.rata_laczna = round((self.kapital * r / (k * (1 - (k / (k + r)) ** n))), 2)
        else:
            raise Exception('Nieznany rodzaj kapitalizacji')

    def sprawdz_stopy_referencyjne(self):
        api_url = 'https://api.api-ninjas.com/v1/interestrate'
        response = requests.get(api_url, headers={'X-Api-Key': 'oqV5jMiQzDrnIXQ7VLaAOQ==ZjesvJ089jrd3D8I'},
                                params={'name': 'polish'})
        if response.status_code == requests.codes.ok:
            rate = response.json()["central_bank_rates"][0]["rate_pct"]
            self.r = rate / 100
        else:
            print("Error:", response.status_code, response.text)

    def generuj_harmonogram(self, oblicz_nowa_laczna: bool = True):

        if oblicz_nowa_laczna:
            self.oblicz_laczna_rate()
        else:
            pass
        self.oblicz_kapitalizacje()
        tabela_splat = self.tabela_splat
        kapital = self.kapital
        rata_laczna = self.rata_laczna
        rata_kapitalowa = self.rata_kapitalowa
        for i in range(self.ilosc_rat - 1):
            numer_raty = i + 1
            k0 = round(kapital * self.kapitalizacja, 2)
            odsetki = round(k0 - kapital, 2)
            if self.rodzaj_rat == RodzajRat.laczne:
                rata_kapitalowa = rata_laczna - odsetki
            elif self.rodzaj_rat == RodzajRat.kapitalowe:
                rata_laczna = rata_kapitalowa + odsetki
            k1 = k0 - rata_laczna
            if k1 < 0:
                continue
            else:
                pass
            tabela_splat.loc[i] = [numer_raty, k0, rata_kapitalowa, odsetki, rata_laczna, k1]
            kapital = k1
        # Ostatnia rata może mieć inną kwotę kapitałową i łączną niż poprzednie raty
        # (kapitału może pozostać mniej lub więcej niż kwota równej raty łącznej
        k0 = round(kapital * self.kapitalizacja, 2)
        odsetki = round(k0 - kapital, 2)
        tabela_splat.loc[self.ilosc_rat - 1] = [self.ilosc_rat, k0, kapital, odsetki, k0, 0]
        tabela_splat['Numer raty'] = tabela_splat['Numer raty'].astype(int)

        return tabela_splat

    def pokaz_harmonogram(self):
        if self.tabela_splat.empty:
            raise Exception("Brak wygenerowanego harmonogramu")
        else:
            print(tabulate(self.tabela_splat, headers='keys', tablefmt='psql'))

    def eksportuj_harmonogram(self, nazwa: str = None):
        if self.tabela_splat.empty:
            raise Exception("Brak wygenerowanego harmonogramu")
        else:
            if nazwa is None:
                self.tabela_splat.to_excel('Harmonogram_splat.xlsx')
            else:
                self.tabela_splat.to_excel(f'{nazwa}.xlsx')

    def oblicz_laczne_odsetki(self):
        if self.tabela_splat.empty:
            raise Exception("Brak wygenerowanego harmonogramu")
        else:
            self.laczne_odsetki = self.tabela_splat['Rata odsetkowa'].sum()
            print(f'Lączne odsetki dla całego kredytu wynoszą: {self.laczne_odsetki}')

    def sprawdz_chronologie_akcji(self, obecna_rata):
        # Sprawdzenie czy ta modyfikacja nie nadpisze poprzednich zmian aby uniknąć zmian na kredycie w 'przeszłości'
        if obecna_rata <= self.ostatnia_zmiana:
            raise Exception('Dokonano już zmian w późniejszych ratach. Zmiana ta nadpisałaby poprzednie zmiany')
        else:
            self.ostatnia_zmiana = obecna_rata

    # Funkcja do liczenia numeru rat pomijając oznaczone nadpłaty i nie licząc ich do rat
    def resetuj_numery_rat(self, kolumna):
        numery = kolumna.copy()
        j = 1
        k = 0
        for i in numery:
            # print(type(i))
            if type(i) == int:
                numery[k] = j
                j += 1
            else:
                pass
            k += 1
        return numery

    def wakacje_kredytowe(self, liczba_rat: int, obecna_rata: int, typ_wakacji: TypWakacji = TypWakacji.rzadowe):
        self.sprawdz_chronologie_akcji(obecna_rata)
        tabela = self.tabela_splat.copy()
        # wyzerowanie harmonogramu abu móc go nadpisać nowymi ratami po wakacjach kredytowych
        self.tabela_splat = pd.DataFrame(columns=tabela.columns)
        if type(tabela) != pd.DataFrame or tabela.empty:
            raise Exception('Nie istnieje Harmonogram spłat do edycji')
        x0 = obecna_rata

        if typ_wakacji == TypWakacji.rzadowe:
            obecny_kapital = round(tabela.loc[x0 - 1]['Kapitał na koniec okresu'], 2)
            nowe_raty = pd.DataFrame({"Numer raty": [i for i in range(liczba_rat)],
                                      "Kapitał na początku okresu": [obecny_kapital for _ in range(liczba_rat)],
                                      "Rata kapitałowa": [0 for _ in range(liczba_rat)],
                                      "Rata odsetkowa": [0 for _ in range(liczba_rat)],
                                      "Rata łączna": [0 for _ in range(liczba_rat)],
                                      "Kapitał na koniec okresu": [obecny_kapital for _ in range(liczba_rat)]})
            nowa_tabela = pd.concat([tabela.iloc[:x0], nowe_raty, tabela.iloc[x0:]]).reset_index(drop=True)
            nowa_tabela["Numer raty"] = self.resetuj_numery_rat(nowa_tabela["Numer raty"])

        elif typ_wakacji == TypWakacji.bankowe:
            obecny_kapital = round(tabela.loc[x0 - 1]['Kapitał na koniec okresu'], 2)
            nowe_raty = pd.DataFrame(
                columns=self.columns)
            for i in range(liczba_rat):
                k0 = round(obecny_kapital, 2)
                k1 = round(obecny_kapital * self.kapitalizacja, 2)
                nowe_raty.loc[i] = [i, k0, 0, 0, 0, k1]
                obecny_kapital = k1

            self.kapital = obecny_kapital
            self.ilosc_rat = int(tabela.index.max()+1) - x0
            kolejne_raty = self.generuj_harmonogram()
            nowa_tabela = pd.concat([self.tabela_splat.iloc[:x0], nowe_raty, kolejne_raty]).reset_index(drop=True)
            nowa_tabela["Numer raty"] = self.resetuj_numery_rat(nowa_tabela["Numer raty"])

        else:
            raise Exception('Nieznany typ wakacji')

        self.tabela_splat = nowa_tabela

    def zmien_oprocentowanie(self, nowy_procent: int = 5, obecna_rata: int = 1,
                             rodzaj_oprocentowania: RodzajOprocentowania = RodzajOprocentowania.stale):
        self.sprawdz_chronologie_akcji(obecna_rata)
        tabela = self.tabela_splat.copy()
        # wyzerowanie harmonogramu abu móc go nadpisać nowymi ratami po zmianie oprocentowania
        self.tabela_splat = pd.DataFrame(columns=tabela.columns)

        if rodzaj_oprocentowania == RodzajOprocentowania.stale:
            self.r = nowy_procent / 100
        elif rodzaj_oprocentowania == RodzajOprocentowania.zmienne:
            self.sprawdz_stopy_referencyjne()
        else:
            raise Exception('Nieznany rodzaj oprocentowania')

        obecny_kapital = round(tabela.loc[obecna_rata - 1]['Kapitał na koniec okresu'], 2)
        self.kapital = obecny_kapital
        self.ilosc_rat = int(tabela.index.max()+1) - obecna_rata
        kolejne_raty = self.generuj_harmonogram()
        nowa_tabela = pd.concat([tabela.iloc[:obecna_rata], kolejne_raty]).reset_index(drop=True)
        nowa_tabela["Numer raty"] = self.resetuj_numery_rat(nowa_tabela["Numer raty"])
        self.tabela_splat = nowa_tabela

    def nadplac_kredyt(self, kwota: float, obecna_rata: int, typ_nadplaty: NadplataKredytu = NadplataKredytu.raty):
        self.sprawdz_chronologie_akcji(obecna_rata)
        tabela = self.tabela_splat.copy()
        # wyzerowanie harmonogramu abu móc go nadpisać nowymi ratami po nadpłacie
        self.tabela_splat = pd.DataFrame(columns=tabela.columns)

        obecny_kapital = round(tabela.loc[obecna_rata - 1]['Kapitał na koniec okresu'], 2)
        self.kapital = obecny_kapital - kwota
        self.ilosc_rat = int(tabela.index.max()+1) - obecna_rata
        if typ_nadplaty == NadplataKredytu.raty:
            kolejne_raty = self.generuj_harmonogram()
        elif typ_nadplaty == NadplataKredytu.okres:
            kolejne_raty = self.generuj_harmonogram(oblicz_nowa_laczna=False)
        else:
            raise Exception('Nieznany typ nadpłaty kredytu')
        nowa_tabela = pd.concat([tabela.iloc[:obecna_rata], kolejne_raty]).reset_index(drop=True)
        nowa_tabela["Numer raty"] = self.resetuj_numery_rat(nowa_tabela["Numer raty"])
        nowa_tabela.loc[obecna_rata-0.5] = ['nadpłata', obecny_kapital, kwota, 0, kwota, obecny_kapital - kwota]
        self.tabela_splat = nowa_tabela.sort_index()

    def zmien_czas_kredytu(self, nowa_liczba_rat: int, obecna_rata: int):
        self.sprawdz_chronologie_akcji(obecna_rata)
        tabela = self.tabela_splat.copy()
        # wyzerowanie harmonogramu abu móc go nadpisać nowymi ratami po zmianie czasu trwania
        self.tabela_splat = pd.DataFrame(columns=tabela.columns)

        obecny_kapital = round(tabela.loc[obecna_rata - 1]['Kapitał na koniec okresu'], 2)
        self.kapital = obecny_kapital
        self.ilosc_rat = nowa_liczba_rat
        kolejne_raty = self.generuj_harmonogram()
        nowa_tabela = pd.concat([tabela.iloc[:obecna_rata], kolejne_raty]).reset_index(drop=True)
        nowa_tabela["Numer raty"] = self.resetuj_numery_rat(nowa_tabela["Numer raty"])
        self.tabela_splat = nowa_tabela
