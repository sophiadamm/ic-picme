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
    plot_discriminante_adams_moulton
)
from pvi.uteis import resolver, tabela_erros, exportar_tabela_discriminante

# ----------------------------- parâmetros ---------------------------------
T  = 1.6                   
TEXP  = 5                   
K  = (0.2, 0.1, 0.05)      
K_REFINADO = (0.0125, 0.00625, 0.003125, 0.0015625)
K_TABELA = (0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625, 0.003125, 0.0015625, 0.00078125, 0.000390625)
PASTA_ITEM = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'item_c'))
PASTA_FIG = os.path.join(PASTA_ITEM, 'figuras')
PASTA_TAB = os.path.join(PASTA_ITEM, 'tabelas')
PASTA_DADOS = os.path.join(PASTA_ITEM, 'dados')
# ---------------------------------------------------------------------------

def executar():
    configurar_estilo()
    prob = motivacao()
    tspan = (prob.t0, T)

    print(f"=== Executando Experimento C (Intervalo Padrão: [0, {T}] e [0, {TEXP}]) ===")

    # 1. Resolução para todos os passos da tabela
    sol_am_tab = [resolver(adams_moulton, prob, k, T) for k in K_TABELA]
    sol_am_tab_exp = [resolver(adams_moulton, prob, k, TEXP) for k in K_TABELA]
    sol_am = sol_am_tab[:len(K)]
    sol_am_exp_padrao = sol_am_tab_exp[:len(K)]
    sol_am_exp_ref = sol_am_tab_exp[4:8]

    # 2. Gráficos de trajetórias
    plot_fig122(prob, sol_am, K, tspan,
                "2-step Adams-Moulton", f"{PASTA_FIG}/c_am")

    tspan_longo = (prob.t0, TEXP)
    plot_fig122(prob, sol_am_exp_padrao, K, tspan_longo,
                "2-step Adams-Moulton", f"{PASTA_FIG}/c_am_T5")    
    plot_fig122(prob, sol_am_exp_ref, K_REFINADO, tspan_longo,
                "2-step Adams-Moulton", f"{PASTA_FIG}/c_am_T5_ref")

    # 3. Análise do Discriminante
    plot_discriminante_adams_moulton(
        prob, 
        K, 
        TEXP+1, 
        f"{PASTA_FIG}/c_discriminante_am_T5", 
        g_func=g, 
        loc_legenda="lower left")

    # 4. Tabela de evolução do discriminante
    exportar_tabela_discriminante(prob, k=0.2, n_passos=3, metodo="adams_moulton", pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)

    # 5. Tabelas de erro computacionalC
    tabela_erros(prob, "2-step Adams-Moulton", sol_am_tab, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)
    tabela_erros(prob, "2-step Adams-Moulton, TF = 5", sol_am_tab_exp, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)

    print("Experimento C (padrão) concluído com sucesso!")

if __name__ == "__main__":
    executar()