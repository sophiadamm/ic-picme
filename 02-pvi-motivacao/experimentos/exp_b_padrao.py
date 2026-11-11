import sys
import os

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))

import matplotlib
matplotlib.use("Agg") 

from pvi.problemas import motivacao
from pvi.metodos import rk4, euler_explicito
from pvi.plotagem import configurar_estilo, plot_fig122
from pvi.uteis import resolver, tabela_erros

# ----------------------------- parâmetros ---------------------------------
T  = 1.6                   
TEXP  = 5                   
K  = (0.2, 0.1, 0.05)      
K_REFINADO = (0.0125, 0.00625, 0.003125, 0.0015625)
K_TABELA = (0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625, 0.003125, 0.0015625, 0.00078125, 0.000390625)
PASTA_ITEM = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'item_b'))
PASTA_FIG = os.path.join(PASTA_ITEM, 'figuras')
PASTA_TAB = os.path.join(PASTA_ITEM, 'tabelas')
PASTA_DADOS = os.path.join(PASTA_ITEM, 'dados')
# ---------------------------------------------------------------------------

def executar():
    configurar_estilo()
    prob = motivacao()
    tspan = (prob.t0, T)

    sol_rk4_tab = [resolver(rk4, prob, k, T) for k in K_TABELA]
    sol_rk4_tab_exp = [resolver(rk4, prob, k, TEXP) for k in K_TABELA]
    sol_rk4 = sol_rk4_tab[:len(K)]
    sol_rk4_exp_padrao = sol_rk4_tab_exp[:len(K)]
    sol_rk4_exp_ref = sol_rk4_tab_exp[4:8]

    plot_fig122(prob, sol_rk4, K, tspan,
                "Runge-Kutta de 4ª Ordem (RK4)", f"{PASTA_FIG}/b_rk4")

    tspan_longo = (prob.t0, TEXP)
    plot_fig122(prob, sol_rk4_exp_padrao, K, tspan_longo,
                "Runge-Kutta de 4ª Ordem (RK4)", f"{PASTA_FIG}/b_rk4_T5")    
    plot_fig122(prob, sol_rk4_exp_ref, K_REFINADO, tspan_longo,
                "Runge-Kutta de 4ª Ordem (RK4)", f"{PASTA_FIG}/b_rk4_T5_ref")
    

    tabela_erros(prob, "Runge-Kutta 4", sol_rk4_tab, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)
    tabela_erros(prob, "Runge-Kutta 4, TF = 5", sol_rk4_tab_exp, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)
    t_rk4_0, U_rk4_0, _ = sol_rk4[0]

if __name__ == "__main__":
    executar()