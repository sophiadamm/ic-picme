from dataclasses import dataclass
from collections.abc import Callable
import numpy as np

@dataclass
class PVI:
    f: Callable[[float, float], float] # y' = f(t,y) 
    dfdy: Callable[[float, float], float]
    y0 : float
    t0: float
    solucao: Callable[[float | np.ndarray], float | np.ndarray] | None
    nome: str

def g(t):
    return (t**4 - 6*t**3 + 12*t**2 - 14*t + 9) / (1 + t)**2

def motivacao() -> PVI:
    def f(t, y):
        return y**2 - g(t)  

    def dfdy(t, y):
        return 2 * y

    def solucao(t):
        return (1 - t) * (2 - t) / (1 + t)
    
    return PVI(f=f, dfdy=dfdy, y0=2.0, t0 = 0.0, solucao=solucao, nome="PVI Motivação")