import sys
import os

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))

import matplotlib
matplotlib.use("Agg") 

from pvi.problemas import motivacao
from pvi.metodos import rk4, euler_implicito
from pvi.plotagem import configurar_estilo, plot_comparacao, plot_fig122
from pvi.uteis import resolver, tabela_erros

# ----------------------------- parâmetros ---------------------------------
TF = 1.6                   
K = (0.2, 0.1, 0.05)      
PASTA_FIG = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'figuras'))
# ---------------------------------------------------------------------------

def executar():
    configurar_estilo()
    prob = motivacao()
    tspan = (prob.t0, TF)

    sol_rk4 = [resolver(rk4, prob, k) for k in K]
    sol_euler = [resolver(euler_implicito, prob, k) for k in K]

    plot_fig122(prob, sol_rk4, K, tspan,
                "Runge-Kutta de 4ª Ordem (RK4)", f"{PASTA_FIG}/b_rk4")

    plot_comparacao(
        prob, sol_rk4, sol_euler, K, tspan,
        titulo1="Runge-Kutta 4 (RK4)", 
        titulo2="Euler recuado (implícito)",
        caminho=f"{PASTA_FIG}/b_comparacao_rk4_euler"
    )

    tabela_erros(prob, "Runge-Kutta 4", sol_rk4, K)

if __name__ == "__main__":
    executar()