from enum import Enum


class RodzajRat(Enum):
    kapitalowe = 'Stałe raty kapitałowe'
    laczne = 'Stałe raty łączne'


class RodzajKapitalizacji(Enum):
    ciagla = 'Kapitalizacja ciągła'
    okresowa = 'Kapitalizacja okresowa'


class OkresyKapitalizacji(Enum):
    dobowa = 360
    tygodniowa = 52
    miesieczna = 12
    kwartalna = 4
    polroczna = 2
    roczna = 1


class OkresSplaty(Enum):
    raty_tygodniowe = 52
    raty_miesieczne = 12
    raty_kwartalne = 4
    raty_roczne = 1


class RodzajOprocentowania(Enum):
    stale = 'oprocentowanie stałe'
    zmienne = 'oprocentowanie zmienne'


class TypWakacji(Enum):
    rzadowe = 'wakacje kredytowe rządowe'
    bankowe = 'wakacje kredytowe bankowe'


class NadplataKredytu(Enum):
    raty = 'zmniejszenie wysokości rat kredytu'
    okres = 'skrócenie czasu trwania kredytu'
