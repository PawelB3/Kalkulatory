import pandas as pd
import numpy_financial as npf
from Parametry import *
from tabulate import tabulate

class Obligacja():

    irr = 0
    duration = 0

    def __init__(self,
                 ilosc: int,
                 wartosc_nominalna: int,
                 termin_za: int,  # czas do terminu wykupu w latach
                 harmonogram:HarmonogramWyplat = HarmonogramWyplat.polroczne,
                 r: float = 0.1):
        self.ilosc = ilosc
        self.nominal = wartosc_nominalna
        self.termin = termin_za
        self.harmonogram = harmonogram
        self.r = r/harmonogram.value
        self.oblicz_irr()
        self.durations()


    def oblicz_irr(self):
        przeplywy = [self.r * self.nominal for _ in range(2 * 3)]
        przeplywy.insert(0, -self.nominal)
        przeplywy.insert(-1, self.nominal * (1 + self.r))
        self.irr = round(npf.irr(przeplywy * self.ilosc), 4)

    def durations(self):
        r = self.r
        m = self.harmonogram.value
        n = m * self.termin
        macaulay_duration = ((1 + r) / (m * r)) * (1 - (1 / (1 + r) ** n))
        modified_duration = macaulay_duration / (1 + r)
        self.duration = round(modified_duration,4)


class PortfelObligacji:

    portfel_irr = 0
    portfel_duration = 0

    def __init__(self):
        self.obligacje = pd.DataFrame(columns=['ilość', 'wartość nominalna',
                                      'częstość wypłat', 'lata do wykupu', 'IRR', 'Śr. czas trwania'])

    def dodaj_obligacje(self, obligacja:Obligacja):
        new_line = [obligacja.ilosc, obligacja.nominal, obligacja.harmonogram.name,
                    obligacja.termin, obligacja.irr, obligacja.duration]
        self.obligacje.loc[len(self.obligacje)] = new_line

    def oblicz_irr(self):
        tabela = self.obligacje
        x1 = ((tabela['ilość'] * tabela['IRR']).sum())
        x2 = (tabela['ilość'].sum())
        self.portfel_irr = round(x1/x2, 4)

    def durations(self):
        tabela = self.obligacje
        x1 = ((tabela['ilość'] * tabela['Śr. czas trwania']).sum())
        x2 = (tabela['ilość'].sum())
        self.portfel_duration = round(x1/x2, 4)

    def portfel_summary(self):
        self.oblicz_irr()
        self.durations()
        print(f'''
        Dla całego portfela wewnętrzna stopu zwrotu wynosi: {self.portfel_irr}
        A średni czas trwania wynosi: {self.portfel_duration}''')
        print(tabulate(self.obligacje, headers='keys', tablefmt='psql'))
