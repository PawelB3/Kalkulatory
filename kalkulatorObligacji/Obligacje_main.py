from Obligacje_class import Obligacja, PortfelObligacji
from Parametry import *

portfel = PortfelObligacji()

portfel.dodaj_obligacje(Obligacja(ilosc=50, wartosc_nominalna=100, termin_za=4,
                                  harmonogram=HarmonogramWyplat.polroczne, r=0.1))

portfel.dodaj_obligacje(Obligacja(ilosc=50, wartosc_nominalna=80, termin_za=2,
                                  harmonogram=HarmonogramWyplat.miesieczne, r=0.08))

portfel.dodaj_obligacje(Obligacja(ilosc=100, wartosc_nominalna=200, termin_za=3,
                                  harmonogram=HarmonogramWyplat.kwartalne, r=0.01))

portfel.portfel_summary()