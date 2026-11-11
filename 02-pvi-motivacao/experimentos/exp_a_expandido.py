import sys
import os

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))

import matplotlib
matplotlib.use("Agg")

from pvi.problemas import motivacao
from pvi.metodos import euler_explicito, euler_implicito
from pvi.plotagem import configurar_estilo, plot_fig122
from pvi.uteis import resolver, tabela_erros

# ----------------------------- parâmetros ---------------------------------
TF = 5.0                   
K = (0.2, 0.1, 0.05)  
K2 = (0.0125, 0.00625, 0.003125, 0.0015625)
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

    print(f"=== Executando Experimento A (Intervalo Expandido: [0, {TF}]) ===")

    # 1. Resolução para todos os passos da tabela no intervalo estendido
    sol_exp_tab = [resolver(euler_explicito, prob, k, TF) for k in K_TABELA]
    sol_imp_tab = [resolver(euler_implicito, prob, k, TF) for k in K_TABELA]

    # 2. Seleção das soluções dos mesmos passos clássicos K = (0.2, 0.1, 0.05) para a Figura 6
    sol_exp_1 = sol_exp_tab[:len(K)]
    sol_imp_1 = sol_imp_tab[:len(K)]

    sol_exp_2 = sol_exp_tab[4:8]
    sol_imp_2 = sol_imp_tab[4:8]

    # 3. Gráficos de longo prazo
    plot_fig122(prob, sol_exp_1, K, tspan,
                "Euler avançado (explícito)", f"{PASTA_FIG}/a_euler_avancadoT5")
    plot_fig122(prob, sol_imp_1, K, tspan,
                "Euler recuado (implícito)", f"{PASTA_FIG}/a_euler_recuadoT5")
    plot_fig122(prob, sol_exp_2, K2, tspan,
                "Euler avançado (explícito)", f"{PASTA_FIG}/a_euler_avancadoT5_ref")
    plot_fig122(prob, sol_imp_2, K2, tspan,
                "Euler recuado (implícito)", f"{PASTA_FIG}/a_euler_recuadoT5_ref")

    # 4. Tabelas de erro computacional em [0, 5]
    tabela_erros(prob, "Euler avançado, TF = 5", sol_exp_tab, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)
    tabela_erros(prob, "Euler recuado, TF = 5", sol_imp_tab, K_TABELA, pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS)

    # 5. Gráficos adicionais com malha refinada fixa (k = 0.000390625)
    k_fixo = K_TABELA[-1]
    sol_exp_fixo = [sol_exp_tab[-1]]
    sol_imp_fixo = [sol_imp_tab[-1]]
    plot_fig122(prob, sol_exp_fixo, (k_fixo,), tspan,
                f"Euler avançado (explícito, k = {k_fixo})", f"{PASTA_FIG}/a_euler_avancado_refinado")
    plot_fig122(prob, sol_imp_fixo, (k_fixo,), tspan,
                f"Euler recuado (implícito, k = {k_fixo})", f"{PASTA_FIG}/a_euler_recuado_refinado")

    print("Experimento do intervalo expandido concluído com sucesso!")

if __name__ == "__main__":
    executar()
