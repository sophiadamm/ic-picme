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
    # --- Metadados opcionais (usados no item d).
    singularidades: tuple[float, ...] = ()
    parar_na_singularidade: bool = True
    # Limiar de |U| acima do qual a trajetória é considerada explodida (None = só inf/NaN).
    limite_explosao: float | None = None

def g(t):
    try:
        return (t**4 - 6*t**3 + 12*t**2 - 14*t + 9) / (1 + t)**2
    except ZeroDivisionError:
        return np.inf

def motivacao(t0: float = 0.0, y0: float | None = None,
              limite_explosao: float | None = None,
              parar_na_singularidade: bool = True) -> PVI:
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
        try:
            return (1 - t) * (2 - t) / (1 + t)
        except ZeroDivisionError:
            return np.inf
    
    if y0 is None:
        y0 = float(solucao(t0))

    return PVI(f=f, dfdy=dfdy, y0=y0, t0=t0, solucao=solucao,
               nome="PVI Motivação",
               singularidades=(-1.0,),
               parar_na_singularidade=parar_na_singularidade,
               limite_explosao=limite_explosao)
