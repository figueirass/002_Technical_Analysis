from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, RSI
import warnings
warnings.simplefilter("ignore")


class SmaCross(Strategy):
    """
    Estrategia de medias moviles simples
    """
    n1 = 5
    n2 = 13

    # Definir Parametros
    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)
    #Definir Estrategia
    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.position.close()

class RsiOscillator(Strategy):
    """
    Estrategia de RSI para detectar sobrecompra y sobreventa
    """
    # Parametros por defecto
    n = 14            # Periodo para el cálculo de RSI
    oversold = 30     # Nivel de sobreventa
    overbought = 70   # Nivel de sobrecompra

    def init(self):
        # Inicializar el indicador RSI
        self.rsi = self.I(RSI, self.data.Close, self.n)

    def next(self):
        # Si el RSI cruza por encima del nivel de sobreventa, comprar
        if crossover(self.oversold, self.rsi):
            self.buy()
        # Si el RSI cruza por debajo del nivel de sobrecompra, cerrar la posición
        elif crossover(self.rsi, self.overbought):
            self.position.close()