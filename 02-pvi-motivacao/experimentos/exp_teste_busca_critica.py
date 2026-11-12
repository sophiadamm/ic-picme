import sys
import os
from pathlib import Path

# Garante que o Python encontre a pasta 'src' ao rodar de 'experimentos/' ou da raiz
DIR_ATUAL = Path(__file__).resolve().parent
sys.path.append(str((DIR_ATUAL / ".." / "src").resolve()))

from pvi.problemas import motivacao
from pvi.uteis import busca_critica

def testar():
    prob = motivacao()
    busca_critica(metodo='euler', tspan=(0, 1.6), prob=prob)
    busca_critica(metodo='euler', tspan=(0, 5), prob=prob)
    busca_critica(metodo='am2', tspan=(0, 5), prob=prob)
    busca_critica(metodo='am2', tspan=(0, 10), prob=prob)

if __name__ == "__main__":
    testar()

