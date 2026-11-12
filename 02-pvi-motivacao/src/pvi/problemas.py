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
        try:
            return y**2 - g(t)
        except OverflowError:
            return np.inf  

    def dfdy(t, y):
        try:
            return 2 * y
        except OverflowError:
            return np.inf

    def solucao(t):
        return (1 - t) * (2 - t) / (1 + t)
    
    return PVI(f=f, dfdy=dfdy, y0=2.0, t0=0.0, solucao=solucao, nome="PVI Motivação")

import numpy as np
# ... (suas importações do PVI)

def dahlquist(lambda_val=-15.0):
    """Problema de teste para região de estabilidade absoluta."""
    f = lambda t, y: lambda_val * y
    dfdy = lambda t, y: lambda_val
    exata = lambda t: np.exp(lambda_val * t)
    
    return PVI(
        t0=0.0, 
        y0=1.0, 
        f=f, 
        dfdy=dfdy, 
        solucao=exata, 
        nome=f"Dahlquist (\u03bb={lambda_val})"
    )