import sys
import os

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))

import matplotlib
matplotlib.use("Agg") 

from pvi.problemas import motivacao
from pvi.metodos import rk4, euler_explicito
from pvi.plotagem import configurar_estilo, plot_comparacao, plot_fig122
from pvi.uteis import resolver, tabela_erros, tabela_passo_a_passo

# ----------------------------- parâmetros ---------------------------------
TF = 1.6                   
K = (0.2, 0.1, 0.05, 0.025, 0.0125)      
K_TABELA = (0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625)
PASTA_ITEM = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'item_b'))
PASTA_FIG = os.path.join(PASTA_ITEM, 'figuras')
PASTA_TAB = os.path.join(PASTA_ITEM, 'tabelas')
PASTA_DADOS = os.path.join(PASTA_ITEM, 'dados')
# ---------------------------------------------------------------------------

def executar():
    configurar_estilo()
    prob = motivacao()
    tspan = (prob.t0, TF)

    sol_rk4_tab = [resolver(rk4, prob, k, TF) for k in K_TABELA]
    sol_euler_tab = [resolver(euler_explicito, prob, k, TF) for k in K_TABELA]
    sol_rk4 = sol_rk4_tab[:len(K)]
    sol_euler = sol_euler_tab[:len(K)]

    plot_fig122(prob, sol_rk4, K, tspan,
                "Runge-Kutta de 4ª Ordem (RK4)", f"{PASTA_FIG}/b_rk4")

    plot_comparacao(
        prob, sol_rk4, sol_euler, K, tspan,
        titulo1="Runge-Kutta 4 (RK4)", 
        titulo2="Euler avançado (explícito)",
        caminho=f"{PASTA_FIG}/b_comparacao_rk4_euler"
    )

    tabela_erros(prob, "Runge-Kutta 4", sol_rk4_tab, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)
    t_rk4_0, U_rk4_0, _ = sol_rk4[0]
    tabela_passo_a_passo(prob, "Runge-Kutta 4", K[0], t_rk4_0, U_rk4_0,
                         export_tex=True, export_csv=True, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)

    # Experimento estendido em [0, 5] para comparação de estabilidade de longo prazo
    TF_LONGO = 5.0
    tspan_longo = (prob.t0, TF_LONGO)
    sol_rk4_T5_tab = [resolver(rk4, prob, k, TF_LONGO) for k in K_TABELA]
    sol_euler_T5_tab = [resolver(euler_explicito, prob, k, TF_LONGO) for k in K_TABELA]
    sol_rk4_T5 = sol_rk4_T5_tab[:len(K)]
    sol_euler_T5 = sol_euler_T5_tab[:len(K)]

    plot_fig122(prob, sol_rk4_T5, K, tspan_longo,
                "Runge-Kutta de 4ª Ordem (RK4)", f"{PASTA_FIG}/b_rk4T5")

    plot_comparacao(
        prob, sol_rk4_T5, sol_euler_T5, K, tspan_longo,
        titulo1="Runge-Kutta 4 (RK4)",
        titulo2="Euler avançado (explícito)",
        caminho=f"{PASTA_FIG}/b_comparacao_rk4_eulerT5"
    )

    tabela_erros(prob, "Runge-Kutta 4, TF = 5", sol_rk4_T5_tab, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)

if __name__ == "__main__":
    executar()