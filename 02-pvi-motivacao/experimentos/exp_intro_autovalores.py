import sys
import os
from pathlib import Path

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = Path(__file__).resolve().parent
sys.path.append(str((DIR_ATUAL / ".." / "src").resolve()))

import matplotlib
matplotlib.use("Agg")

from pvi.problemas import motivacao
from pvi.plotagem import (
    configurar_estilo,
    plot_autovalor_assintotas,
    plot_autovalor_individual,
)

# ----------------------------- parâmetros ---------------------------------
X_LIM_GLOBAL = (-5.0, 40.0)
X_LIM_ZOOM = (-1.5, 5.0)
PASTA_FIG = (DIR_ATUAL / ".." / "resultados" / "introducao" / "figuras").resolve()
# ---------------------------------------------------------------------------


def executar():
    configurar_estilo()
    prob = motivacao()

    PASTA_FIG.mkdir(parents=True, exist_ok=True)

    # 1) Figura combinada com os 2 painéis lado a lado (Visão Global e Detalhe Local)
    caminho_fig = str(PASTA_FIG / "intro_autovalores")
    plot_autovalor_assintotas(
        prob,
        caminho=caminho_fig,
        x_lim_global=X_LIM_GLOBAL,
        x_lim_zoom=X_LIM_ZOOM,
    )
    print(f"Salvo: {caminho_fig}.pdf e .png (painéis combinados)")

    # 2) Figuras individuais para cada intervalo de interesse
    caminho_global = str(PASTA_FIG / "intro_autovalor_global")
    caminho_zoom = str(PASTA_FIG / "intro_autovalor_zoom")
    plot_autovalor_individual(
        prob,
        caminho_global=caminho_global,
        caminho_zoom=caminho_zoom,
        x_lim_global=X_LIM_GLOBAL,
        x_lim_zoom=X_LIM_ZOOM,
    )

if __name__ == "__main__":
    executar()
