from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter("ignore")


def rsi(array: np.ndarray, n: int = 14) -> np.ndarray:
    """
    Calcula el Índice de Fuerza Relativa (RSI) manualmente usando Pandas.
    """
    # Convertir el array de numpy a una serie de pandas para facilitar los cálculos
    prices = pd.Series(array)
    
    # 1. Calcular cambios de precio
    delta = prices.diff()

    # 2. Separar ganancias y pérdidas
    gain = delta.clip(lower=0)
    loss = -1 * delta.clip(upper=0)

    # 3. Calcular la media móvil exponencial de ganancias y pérdidas (Wilder's smoothing)
    avg_gain = gain.ewm(com=n - 1, min_periods=n).mean()
    avg_loss = loss.ewm(com=n - 1, min_periods=n).mean()
    
    # 4. Calcular RS (Relative Strength) y el RSI final
    rs = avg_gain / avg_loss
    rsi_series = 100 - (100 / (1 + rs))
    
    # La función debe devolver un array de numpy para que backtesting.py lo procese
    return rsi_series.to_numpy()


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
    n = 14
    oversold = 30
    overbought = 70

    def init(self):
        # Usamos nuestra implementación manual de RSI
        self.rsi = self.I(rsi, self.data.Close, self.n)

    def next(self):
        if crossover(self.oversold, self.rsi):
            self.buy()
        elif crossover(self.rsi, self.overbought):
            self.position.close()