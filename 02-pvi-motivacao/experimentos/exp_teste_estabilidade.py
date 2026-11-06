import sys
import os

DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))

import matplotlib
matplotlib.use("Agg") 

from pvi.problemas import dahlquist
from pvi.metodos import euler_explicito, euler_implicito
from pvi.plotagem import configurar_estilo, plot_comparacao
from pvi.uteis import resolver, tabela_erros

# ----------------------------- parâmetros ---------------------------------
TF = 1.0                   
KS = (0.2, 0.15, 0.1, 0.05)  # Cruzando a fronteira crítica de k=0.133
PASTA_FIG = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'figuras'))
# ---------------------------------------------------------------------------

def executar():
    configurar_estilo()
    # Cria o problema com um decaimento abrupto (stiff)
    prob = dahlquist(lambda_val=-15.0)
    tspan = (prob.t0, TF)

    sol_exp = [resolver(euler_explicito, prob, k, TF) for k in KS]
    sol_imp = [resolver(euler_implicito, prob, k, TF) for k in KS]

    plot_comparacao(
        prob, sol_exp, sol_imp, KS, tspan,
        titulo1="Euler Explícito (Instabilidade)", 
        titulo2="Euler Implícito (Incondicionalmente Estável)",
        caminho=f"{PASTA_FIG}/d_comparacao_estabilidade"
    )

    tabela_erros(prob, "Euler Explícito", sol_exp, KS)
    tabela_erros(prob, "Euler Implícito", sol_imp, KS)

if __name__ == "__main__":
    executar()