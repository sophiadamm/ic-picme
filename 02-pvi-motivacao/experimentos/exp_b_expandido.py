import sys
import os

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))

import matplotlib
matplotlib.use("Agg") 

from pvi.problemas import motivacao, g
from pvi.metodos import rk4
from pvi.plotagem import configurar_estilo, plot_fig122, plot_isoclinas
from pvi.uteis import resolver, tabela_erros, diagnosticar_cruzamento_isoclina

# ----------------------------- parâmetros ---------------------------------
TF = 10.0                   
K =  (0.00625, 0.003125, 0.0015625)
K_TABELA = (0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625, 0.003125, 0.0015625, 0.00078125, 0.000390625)
PASTA_ITEM = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'item_b'))
PASTA_FIG = os.path.join(PASTA_ITEM, 'figuras')
PASTA_TAB = os.path.join(PASTA_ITEM, 'tabelas')
PASTA_DADOS = os.path.join(PASTA_ITEM, 'dados')
# ---------------------------------------------------------------------------

def executar():
    configurar_estilo()
    prob = motivacao()
    tspan = (prob.t0, TF)

    # 1. Resolução para todos os passos da tabela no intervalo estendido
    sol_rk4_tab = [resolver(rk4, prob, k, TF) for k in K_TABELA]

    # 2. Seleção das soluções dos mesmos passos clássicos K = (0.2, 0.1, 0.05) para a Figura 6
    sol_rk4_1 = sol_rk4_tab[:len(K)]

    sol_rk4_2 = sol_rk4_tab[4:8]

    # 3. Gráficos de longo prazo
    plot_fig122(prob, sol_rk4_1, K, tspan,
                "Runge-Kutta de 4ª Ordem (RK4)", f"{PASTA_FIG}/b_rk4T10")

    # 4. Tabelas de erro computacional em [0, 10]
    tabela_erros(prob, "Runge-Kutta 4, TF = 10", sol_rk4_tab, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)

    # 5. Gráfico das Isóclinas
    caminho_fig2 =  os.path.join(PASTA_FIG, "b_isoclinas_rk4")
    plot_isoclinas(
        prob,
        rk4,
        K,
        TF,
        caminho_fig2,
        titulo="Runge-Kutta 4 (Refinado)",
        g_func=g,
        x_lim_zoom=(6.5, 8),     
        ylim=(-3.0, 4.8),          
        ylim_zoom=(2.5, 4.6),     
    )
    diagnosticar_cruzamento_isoclina(prob, rk4, K_TABELA, tf=TF)

if __name__ == "__main__":
    executar()
