import sys
from pathlib import Path

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = Path(__file__).resolve().parent
sys.path.append(str((DIR_ATUAL / ".." / "src").resolve()))

import matplotlib
matplotlib.use("Agg")
import numpy as np

from pvi.problemas import motivacao, g
from pvi.metodos import euler_explicito
from pvi.plotagem import configurar_estilo, plot_isoclinas
from pvi.uteis import resolver

# ----------------------------- parâmetros ---------------------------------
TF = 5.0
K = (0.2, 0.1, 0.05)
K_REFINADO = (0.0125, 0.00625, 0.003125, 0.0015625)
PASTA_ITEM = (DIR_ATUAL / ".." / "resultados" / "item_a").resolve()
PASTA_FIG = PASTA_ITEM / "figuras"
# ---------------------------------------------------------------------------

def diagnosticar_cruzamento_isoclina(prob, metodo, ks, tf=5.0):
    """Imprime o diagnóstico do instante em que cada trajetória cruza a isóclina +sqrt(g(t))."""
    print(f"=== Diagnóstico de Cruzamento da Isóclina +sqrt(g(t)) em [0, {tf}] ===")
    for k in ks:
        t, U, _ = resolver(metodo, prob, k, tf)
        # Busca em t > 3.5 onde f(t_n, U_n) = U_n^2 - g(t_n) fica negativo
        mask = t > 3.5
        t_pos = t[mask]
        U_pos = U[mask]
        f_pos = U_pos**2 - g(t_pos)

        idx_neg = np.where(f_pos < 0)[0]
        idx_pico = np.argmax(U_pos)
        t_pico = t_pos[idx_pico]
        u_pico = U_pos[idx_pico]
        iso_pico = np.sqrt(max(g(t_pico), 0.0))

        if len(idx_neg) > 0:
            t_cruz = t_pos[idx_neg[0]]
            print(
                f"k = {k:<10} | Pico em t = {t_pico:.4f} (U = {u_pico:.4f}, +sqrt(g) = {iso_pico:.4f}) "
                f"| Mergulho (f < 0) a partir de t = {t_cruz:.4f} | U(5) = {U[-1]:+.4f}"
            )
        else:
            print(f"k = {k:<10} | Permaneceu acima da isóclina até t = {tf} | U(5) = {U[-1]:+.4f}")


def executar():
    configurar_estilo()
    prob = motivacao()

    # 1. Gráfico de isóclinas para os passos clássicos K = (0.2, 0.1, 0.05)
    caminho_fig1 = PASTA_FIG / "a_isoclinas_eulerT5"
    plot_isoclinas(
        prob,
        euler_explicito,
        K,
        TF,
        caminho_fig1,
        titulo="Euler Avançado",
        g_func=g,
        x_lim_zoom=(3.0, 5.0),
    )
    print(f"Figura salva em: {caminho_fig1}.png / .pdf")

    # 2. Gráfico de isóclinas para as malhas refinadas K_REFINADO
    caminho_fig2 = PASTA_FIG / "a_isoclinas_eulerT5_refinado"
    plot_isoclinas(
        prob,
        euler_explicito,
        K_REFINADO,
        TF,
        caminho_fig2,
        titulo="Euler Avançado (Refinado)",
        g_func=g,
        x_lim_zoom=(3.2, 5.0),
    )
    print(f"Figura salva em: {caminho_fig2}.png / .pdf\n")

    diagnosticar_cruzamento_isoclina(prob, euler_explicito, K + K_REFINADO, tf=TF)


if __name__ == "__main__":
    executar()

