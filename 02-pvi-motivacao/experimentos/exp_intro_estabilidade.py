import sys
from pathlib import Path

# Garante que os caminhos sejam resolvidos em relação à pasta do script
DIR_ATUAL = Path(__file__).resolve().parent
sys.path.append(str((DIR_ATUAL / ".." / "src").resolve()))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad

# ----------------------------- parâmetros ---------------------------------
# Garante que os resultados vão para resultados/introducao/figuras na raiz do projeto
PASTA = (DIR_ATUAL / ".." / "resultados" / "introducao" / "figuras").resolve()

# Figura: Fio da Navalha
DELTA_B = 1e-4             # perturbação inicial: y(0) = 2 +- DELTA_B
XMAX_B = 9.0
YB = (-7.0, 8.0)
N_PONTOS = 3001            # pontos da malha de plotagem em [0, XMAX_B]
# ---------------------------------------------------------------------------


# ----------------------------- funções do problema -------------------------
def g(x):
    return (x**4 - 6*x**3 + 12*x**2 - 14*x + 9) / (1 + x)**2


def y_exata(x):
    return (1 - x) * (2 - x) / (1 + x)


def lam(x):
    """Autovalor local: lambda(x) = df/dy ao longo da exata = 2 y(x)."""
    return 2 * y_exata(x)


def Phi(x):
    """Primitiva de lambda com Phi(0) = 0."""
    return x**2 - 8*x + 12*np.log1p(x)


def integral_I(xs):
    """I(x) = int_0^x exp(Phi) nos pontos xs (crescentes, xs[0] = 0)."""
    I = np.zeros_like(xs)
    for i in range(1, len(xs)):
        I[i] = I[i - 1] + quad(lambda s: np.exp(Phi(s)), xs[i - 1], xs[i])[0]
    return I


def solucao_perturbada(xs, I, delta):
    """w(x) = y(x) + eps(x) com w(0) = 2 + delta. NaN após a explosão."""
    den = 1 - delta * I
    w = np.full_like(xs, np.nan)
    ok = den > 0
    w[ok] = y_exata(xs[ok]) + delta * np.exp(Phi(xs[ok])) / den[ok]
    return w


def x_explosao(delta, xs, I):
    """x* tal que delta * I(x*) = 1 (só vale para delta > 0)."""
    return np.interp(np.log(1 / delta), np.log(I[1:]), xs[1:])


# ----------------------------- utilidades de figura -----------------------
def configurar_estilo():
    plt.rcParams.update({
        "figure.dpi": 110, "font.size": 11, "axes.grid": True,
        "grid.alpha": 0.3, "savefig.bbox": "tight",
    })


def salvar(fig, nome):
    PASTA.mkdir(parents=True, exist_ok=True)
    fig.savefig(PASTA / f"{nome}.pdf")
    fig.savefig(PASTA / f"{nome}.png", dpi=200)
    plt.close(fig)


def verificar_formula():
    """Confere (por diferenças centrais) que w satisfaz w' = w^2 - g."""
    def I_ponto(x):
        return quad(lambda s: np.exp(Phi(s)), 0, x)[0]

    def w(x, d):
        return y_exata(x) + d * np.exp(Phi(x)) / (1 - d * I_ponto(x))

    pior, h = 0.0, 1e-5
    for d in (DELTA_B, -DELTA_B):
        for x in (0.5, 1.3, 2.5, 4.0):
            dw = (w(x + h, d) - w(x - h, d)) / (2 * h)
            pior = max(pior, abs(dw - (w(x, d)**2 - g(x))) / (1 + abs(dw)))
    print(f"[verificação] maior resíduo relativo da EDO: {pior:.1e}")
    assert pior < 1e-6, "a fórmula fechada não satisfaz a EDO"


# ----------------------------- Figura: fio da navalha ---------------------
def fig_fio_navalha(xs, I):
    wp = solucao_perturbada(xs, I, +DELTA_B)
    wn = solucao_perturbada(xs, I, -DELTA_B)
    xb = x_explosao(DELTA_B, xs, I)
    expo = int(round(np.log10(DELTA_B)))

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    ax.plot(xs, wp, color="tab:red", lw=1.8,
            label=rf"$y(0)=2+10^{{{expo}}}$")
    ax.plot(xs, wn, color="tab:blue", lw=1.8,
            label=rf"$y(0)=2-10^{{{expo}}}$")
    ax.plot(xs, y_exata(xs), "k", lw=1.6, ls=(0, (4, 2)),
            label=r"exata, $y(0)=2$")
    ax.axhline(0, color="k", lw=0.6)

    ax.annotate(rf"explode em $x\approx{xb:.1f}$".replace(".", "{,}"),
                (xb, YB[1] - 0.2), xytext=(-105, -18), textcoords="offset points",
                fontsize=10, color="tab:red",
                arrowprops=dict(arrowstyle="->", color="tab:red", lw=0.9))
    ax.annotate(r"desce para $y\approx4-x$", (7.2, -3.3), xytext=(-20, -48),
                textcoords="offset points", fontsize=10, color="tab:blue",
                arrowprops=dict(arrowstyle="->", color="tab:blue", lw=0.9))

    ax.set_xlim(0, XMAX_B)
    ax.set_ylim(*YB)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("Uma perturbação de 0,005% na condição inicial")
    ax.legend(loc="upper left", fontsize=9.5)
    salvar(fig, "figB_fio_navalha")
    print(f"[figB] x* para delta = {DELTA_B:g}: {xb:.3f}")


def main():
    configurar_estilo()
    verificar_formula()
    xs = np.linspace(0.0, XMAX_B, N_PONTOS)
    I = integral_I(xs)
    fig_fio_navalha(xs, I)
    print(f"Figura salva em {PASTA}/figB_fio_navalha (.pdf e .png)")


if __name__ == "__main__":
    main()
