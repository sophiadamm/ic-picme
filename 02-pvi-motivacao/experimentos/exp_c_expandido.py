import sys
import os

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))

import matplotlib
matplotlib.use("Agg") 

from pvi.problemas import motivacao, g
from pvi.metodos import adams_moulton
from pvi.plotagem import (
    configurar_estilo,
    plot_fig122,
    plot_discriminante_adams_moulton,
)
from pvi.uteis import resolver, tabela_erros

# ----------------------------- parâmetros ---------------------------------
TF = 10.0                   
K =  (0.00625, 0.003125, 0.0015625)
K_TABELA = (0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625, 0.003125, 0.0015625, 0.00078125, 0.000390625)
PASTA_ITEM = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'item_c'))
PASTA_FIG = os.path.join(PASTA_ITEM, 'figuras')
PASTA_TAB = os.path.join(PASTA_ITEM, 'tabelas')
PASTA_DADOS = os.path.join(PASTA_ITEM, 'dados')
# ---------------------------------------------------------------------------

def executar():
    configurar_estilo()
    prob = motivacao()
    tspan = (prob.t0, TF)

    print(f"=== Executando Experimento C (Intervalo Expandido: [0, {TF}]) ===")

    # 1. Resolução para todos os passos da tabela no intervalo estendido
    sol_am_tab = [resolver(adams_moulton, prob, k, TF) for k in K_TABELA]

    # 2. Seleção das soluções dos passos refinados para a Figura
    sol_am_1 = sol_am_tab[:len(K)]
    sol_am_2 = sol_am_tab[4:8]

    # 3. Gráficos de longo prazo
    plot_fig122(prob, sol_am_1, K, tspan,
                "2-step Adams-Moulton", f"{PASTA_FIG}/c_am_T10")

    # 4. Tabelas de erro computacional em [0, 10]
    tabela_erros(prob, "2-step Adams-Moulton, TF = 10", sol_am_tab, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)

    # 5. Gráfico do Discriminante em [0, 10]
    caminho_fig_disc = os.path.join(PASTA_FIG, "c_discriminante_am_T10")
    plot_discriminante_adams_moulton(
        prob, 
        K, TF, 
        caminho_fig_disc, 
        g_func=g,
        loc_legenda="lower left"
    )

if __name__ == "__main__":
    executar()
