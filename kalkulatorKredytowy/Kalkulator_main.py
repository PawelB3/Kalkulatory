from Kalkulator_klasa import Kalkulator
from parametry import *
# Instrukcja
#   Parametry startowe kalkulatora:
#       kwota kredytu
#       ilość rat -podana jako ilość okresów spłaty -nie większa niż 35 lat
#       okres spłat (możliwe raty tygodniowe, miesięczne (domyślnie), kwartalne i roczne)
#       rodzaj rat (raty ze stałą kwotą łączną -raty stałe (domyślnie) lub ze stałą kwotą kapitałową -raty malejące
#       rodzaj oprocentowania -stałe lub zmienne (domyślnie) -stałe używa wartości stopa_procentowa,
#           zmienne pobiera obecną stopę referencyjną NBP -nie znalazłem API z WIBOR
#       rodzaj kapitalizacji -kapitalizacja ciągła (domyślnie) lub okresowa
#       okres kapitalizacji -okresy kapitalizacji, jeśli kapitalizacja okresowa jest używana
#           (możliwa kapitalizacja dobowa, tygodniowa, miesięczna (domyślnie), kwartalna, półroczna i roczna)
#
#   Możliwe operacje na wygenerowanym harmonogramie
#       wakacje kredytowe
#           wakacje rządowe -odsetki nie są naliczane, kapitał do spłaty się nie zmienia
#           wakacje bankowe -odsetki są doliczane do kapitału
#       nadpłata kredytu
#           nadpłata zmniejszająca przyszły raty kredytu
#           nadpłata zmniejszająca okres trwania kredytu - zmniejsza liczbę rat do spłaty
#       zmiana oprocentowania
#           zmiana oprocentowania stałego - podanie nowego oprocentowania
#           aktualizacja oprocentowania zmiennego - pobiera aktualną wartość stopy referencyjnej
#       zmiana czasu kredytu -pozwala na zmianę ilości pozostałych do spłaty rat (wydłuża lub skraca kredyt)
#       łączne odsetki -oblicza sumy wszystkich odsetek jakie trzeba będzie zapłacić w czasie trwania całego kredytu
#       eksport harmonogramu -pozwala na zapisanie wygenerowanego harmonogramu w formacie Excel
#
# Przykład 1
kalkulator = Kalkulator(
    kwota_kredytu=720000,
    ilosc_rat=300,
    okres_splat=OkresSplaty.raty_miesieczne,
    rodzaj_rat=RodzajRat.laczne,
    rodzaj_oprocentowania=RodzajOprocentowania.stale,
    stopa_procentowa=9.25,
    r_kapitalizacji=RodzajKapitalizacji.ciagla,
    okres_kapitalizacji=OkresyKapitalizacji.miesieczna  # okresy nieużywanie w przypadku kapitalizacji ciągłej
)

kalkulator.generuj_harmonogram()
print('Odsetki przed wakacjami/nadpłatami:')
kalkulator.oblicz_laczne_odsetki()

kalkulator.wakacje_kredytowe(liczba_rat=5, obecna_rata=10, typ_wakacji=TypWakacji.rzadowe)
kalkulator.nadplac_kredyt(kwota=20000, obecna_rata=20, typ_nadplaty=NadplataKredytu.raty)
kalkulator.nadplac_kredyt(kwota=20000, obecna_rata=40, typ_nadplaty=NadplataKredytu.okres)
kalkulator.zmien_oprocentowanie(nowy_procent=8, obecna_rata=70)
kalkulator.zmien_czas_kredytu(nowa_liczba_rat=150, obecna_rata=100)
kalkulator.pokaz_harmonogram()
print('Odsetki końcowe:')
kalkulator.oblicz_laczne_odsetki()
kalkulator.eksportuj_harmonogram()

# Przykład 2
print('Przykład 2')
kalkulator2 = Kalkulator(
    kwota_kredytu=380000,
    ilosc_rat=250,
    okres_splat=OkresSplaty.raty_miesieczne,
    rodzaj_rat=RodzajRat.kapitalowe,
    rodzaj_oprocentowania=RodzajOprocentowania.zmienne,
    r_kapitalizacji=RodzajKapitalizacji.okresowa,
    okres_kapitalizacji=OkresyKapitalizacji.miesieczna  # okresy nieużywanie w przypadku kapitalizacji ciągłej
)
kalkulator2.generuj_harmonogram()
print('Odsetki przed wakacjami/nadpłatami:')
kalkulator2.oblicz_laczne_odsetki()
kalkulator2.wakacje_kredytowe(liczba_rat=6, obecna_rata=15, typ_wakacji=TypWakacji.bankowe)
kalkulator2.nadplac_kredyt(kwota=10000, obecna_rata=40, typ_nadplaty=NadplataKredytu.okres)
kalkulator2.zmien_oprocentowanie(nowy_procent=8, obecna_rata=60, rodzaj_oprocentowania=RodzajOprocentowania.stale)
kalkulator2.zmien_czas_kredytu(nowa_liczba_rat=180, obecna_rata=90)
kalkulator2.nadplac_kredyt(kwota=5000,obecna_rata=130, typ_nadplaty=NadplataKredytu.raty)
kalkulator2.pokaz_harmonogram()
print('Odsetki końcowe:')
kalkulator2.oblicz_laczne_odsetki()
kalkulator2.eksportuj_harmonogram(nazwa='Harmonogram2')