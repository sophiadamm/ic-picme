import sys
import os
# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import matplotlib
matplotlib.use("Agg") 

from pvi.problemas import motivacao
from pvi.metodos import euler_explicito, euler_implicito
from pvi.plotagem import configurar_estilo, plot_comparacao, plot_fig122
from pvi.uteis import resolver, tabela_erros, tabela_passo_a_passo # Importando as ferramentas universais

# ----------------------------- parâmetros ---------------------------------
TF = 1.6                   
K = (0.2, 0.1, 0.05)      
PASTA_FIG = "../resultados/figuras" # Ajustado para refletir a nova pasta relativa
# ---------------------------------------------------------------------------

def executar():
    configurar_estilo()
    prob = motivacao()
    tspan = (prob.t0, TF)

    sol_exp = [resolver(euler_explicito, prob, k) for k in K]
    sol_imp = [resolver(euler_implicito, prob, k) for k in K]

    plot_fig122(prob, sol_exp, K, tspan,
                "Euler avançado (explícito)", f"{PASTA_FIG}/a_euler_avancado")
    plot_fig122(prob, sol_imp, K, tspan,
                "Euler recuado (implícito)", f"{PASTA_FIG}/a_euler_recuado")
    plot_comparacao(prob, sol_exp, sol_imp, K, tspan,
                    f"{PASTA_FIG}/a_comparacao")

    tabela_erros(prob, "Euler avançado", sol_exp, K)
    tabela_erros(prob, "Euler recuado", sol_imp, K)

    # for i_k in [0, 1]:  
    #     k_atual = K[i_k]
        
    #     t_exp, U_exp, _ = sol_exp[i_k]
    #     t_imp, U_imp, _ = sol_imp[i_k]
        
    #     tabela_passo_a_passo(prob, "Euler avancado", k_atual, t_exp, U_exp, 
    #                          export_tex=i_k^1, export_csv=True)
    #     tabela_passo_a_passo(prob, "Euler recuado", k_atual, t_imp, U_imp, 
    #                          export_tex=i_k^1, export_csv=True)

if __name__ == "__main__":
    executar()