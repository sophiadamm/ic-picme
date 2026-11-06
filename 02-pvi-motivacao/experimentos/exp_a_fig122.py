import sys
import os
# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))
import matplotlib
matplotlib.use("Agg") 

from pvi.problemas import motivacao
from pvi.metodos import euler_explicito, euler_implicito
from pvi.plotagem import configurar_estilo, plot_comparacao, plot_fig122
from pvi.uteis import resolver, tabela_erros, tabela_passo_a_passo # Importando as ferramentas universais

# ----------------------------- parâmetros ---------------------------------
TF = 1.6                   
K = (0.2, 0.1, 0.05)      
K_TABELA = (0.2, 0.1, 0.05, 0.025, 0.0125, 0.00625)
PASTA_FIG = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'figuras'))
# ---------------------------------------------------------------------------

def executar():
    configurar_estilo()
    prob = motivacao()
    tspan = (prob.t0, TF)

    sol_exp_tab = [resolver(euler_explicito, prob, k, TF) for k in K_TABELA]
    sol_imp_tab = [resolver(euler_implicito, prob, k, TF) for k in K_TABELA]
    sol_exp = sol_exp_tab[:len(K)]
    sol_imp = sol_imp_tab[:len(K)]

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

    tabela_erros(prob, "Euler avançado", sol_exp_tab, K_TABELA)
    tabela_erros(prob, "Euler recuado", sol_imp_tab, K_TABELA)

    for i_k in [0, 1]:  
        k_atual = K[i_k]
        
        t_exp, U_exp, _ = sol_exp[i_k]
        t_imp, U_imp, _ = sol_imp[i_k]
        
        tabela_passo_a_passo(prob, "Euler avancado", k_atual, t_exp, U_exp, 
                             export_tex=(i_k == 0), export_csv=True)
        tabela_passo_a_passo(prob, "Euler recuado", k_atual, t_imp, U_imp, 
                             export_tex=(i_k == 0), export_csv=True)

    # Experimento estendido em [0, 5]
    TF_LONGO = 5.0
    tspan_longo = (prob.t0, TF_LONGO)
    sol_exp_T5_tab = [resolver(euler_explicito, prob, k, TF_LONGO) for k in K_TABELA]
    sol_imp_T5_tab = [resolver(euler_implicito, prob, k, TF_LONGO) for k in K_TABELA]
    sol_exp_T5 = sol_exp_T5_tab[:len(K)]
    sol_imp_T5 = sol_imp_T5_tab[:len(K)]

    plot_fig122(prob, sol_exp_T5, K, tspan_longo,
                "Euler avançado (explícito)", f"{PASTA_FIG}/a_euler_avancadoT5")
    plot_fig122(prob, sol_imp_T5, K, tspan_longo,
                "Euler recuado (implícito)", f"{PASTA_FIG}/a_euler_recuadoT5")

    tabela_erros(prob, "Euler avançado, TF = 5", sol_exp_T5_tab, K_TABELA)
    tabela_erros(prob, "Euler recuado, TF = 5", sol_imp_T5_tab, K_TABELA)

if __name__ == "__main__":
    executar()