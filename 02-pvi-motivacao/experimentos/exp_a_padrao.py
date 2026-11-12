import sys
import os

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))

import matplotlib
matplotlib.use("Agg")

from pvi.problemas import motivacao, g
from pvi.metodos import euler_explicito, euler_implicito
from pvi.plotagem import (
    configurar_estilo,
    plot_comparacao,
    plot_fig122,
    plot_discriminante_euler,
)
from pvi.uteis import resolver, tabela_erros, tabela_passo_a_passo, exportar_tabela_discriminante

# ----------------------------- parâmetros ---------------------------------
TF = 1.6
K = (0.2, 0.1, 0.05)
K_TABELA = (0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625, 0.003125, 0.0015625, 0.00078125, 0.000390625)
PASTA_ITEM = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'item_a'))
PASTA_FIG = os.path.join(PASTA_ITEM, 'figuras')
PASTA_TAB = os.path.join(PASTA_ITEM, 'tabelas')
PASTA_DADOS = os.path.join(PASTA_ITEM, 'dados')
# ---------------------------------------------------------------------------

def executar():
    configurar_estilo()
    prob = motivacao()
    tspan = (prob.t0, TF)

    print(f"=== Executando Experimento A (Intervalo Padrão: [0, {TF}]) ===")

    # 1. Resolução para todos os passos da tabela
    sol_exp_tab = [resolver(euler_explicito, prob, k, TF) for k in K_TABELA]
    sol_imp_tab = [resolver(euler_implicito, prob, k, TF) for k in K_TABELA]

    # 2. Seleção das soluções dos 3 passos clássicos para plotagem (Figura 12.2)
    sol_exp = sol_exp_tab[:len(K)]
    sol_imp = sol_imp_tab[:len(K)]

    # 3. Gráficos individuais e comparação lado a lado
    plot_fig122(prob, sol_exp, K, tspan,
                "Euler avançado (explícito)", f"{PASTA_FIG}/a_euler_avancado")
    plot_fig122(prob, sol_imp, K, tspan,
                "Euler recuado (implícito)", f"{PASTA_FIG}/a_euler_recuado")
    plot_comparacao(
        prob, sol_exp, sol_imp, K, tspan,
        titulo1="Euler avançado (explícito)", 
        titulo2="Euler recuado (implícito)",
        caminho=f"{PASTA_FIG}/a_comparacao"
    )

    # 4. Análise do Discriminante no intervalo padrão [0, 1.6]
    plot_discriminante_euler(prob, K, TF, f"{PASTA_FIG}/a_discriminante_euler", g_func=g, loc_legenda="lower right")
    exportar_tabela_discriminante(prob, k=0.2, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)

    # 5. Tabelas de erro e convergência assintótica
    tabela_erros(prob, "Euler avançado", sol_exp_tab, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)
    tabela_erros(prob, "Euler recuado", sol_imp_tab, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)

    # 6. Tabelas passo a passo dos primeiros passos
    for i_k in [0, 1]:  
        k_atual = K[i_k]
        t_exp, U_exp, _ = sol_exp[i_k]
        t_imp, U_imp, _ = sol_imp[i_k]
        
        tabela_passo_a_passo(prob, "Euler avancado", k_atual, t_exp, U_exp, 
                             export_tex=(i_k == 0), export_csv=True,
                             pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)
        tabela_passo_a_passo(prob, "Euler recuado", k_atual, t_imp, U_imp, 
                             export_tex=(i_k == 0), export_csv=True,
                             pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)

    print("Experimento do intervalo padrão concluído com sucesso!")


if __name__ == "__main__":
    executar()
