import sys
import os

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))

import matplotlib
matplotlib.use("Agg")

from pvi.problemas import motivacao
from pvi.plotagem import configurar_estilo, plot_solucao_assintotas

# ----------------------------- parâmetros ---------------------------------
# enunciado: [-5, 40], [-2, 2], [0, 5] e [0, 1.6]
X_LIM_GLOBAL = (-5.0, 40.0)
# Intervalo de zoom para destacar o entorno da singularidade e os regimes locais dos experimentos
X_LIM_ZOOM = (-1.5, 5.0)
PASTA_FIG = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'introducao', 'figuras'))
# ---------------------------------------------------------------------------


def executar():
    configurar_estilo()
    prob = motivacao()
    caminho_fig = os.path.join(PASTA_FIG, "intro_solucao_assintotas")
    plot_solucao_assintotas(
        prob,
        caminho=caminho_fig,
        x_lim_global=X_LIM_GLOBAL,
        x_lim_zoom=X_LIM_ZOOM,
    )


if __name__ == "__main__":
    executar()
