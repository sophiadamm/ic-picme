import sys
import os
import argparse
from pathlib import Path

# Garante que o Python encontre a pasta 'src' ao rodar de dentro de 'experimentos/' ou da raiz
DIR_ATUAL = Path(__file__).resolve().parent
ROOT_DIR = DIR_ATUAL.parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import matplotlib
matplotlib.use("Agg")

from pvi.problemas import motivacao
from pvi.metodos import euler_explicito, euler_implicito, rk4, adams_moulton
from pvi.plotagem import plot_k_fixo, plot _k_fixo, configurar_estilo

# ---------------------------------------------------------------------------
# Mapeamento de métodos disponíveis
# ---------------------------------------------------------------------------
METODOS_MAP = {
    "euler_explicito": euler_explicito,
    "euler_implicito": euler_implicito,
    "rk4": rk4,
    "adams_moulton": adams_moulton,
    # Aliases
    "euler": euler_explicito,
    "fe": euler_explicito,
    "be": euler_implicito,
    "am": adams_moulton,
    "am2": adams_moulton,
}

# ----------------------------- parâmetros padrão ---------------------------
TF_PADRAO = 1.6
K_PADRAO = 0.05
METODOS_PADRAO = ["euler_explicito", "euler_implicito", "rk4", "adams_moulton"]

PASTA_UTILITARIOS = ROOT_DIR / "resultados" / "utilitarios"
PASTA_FIG = PASTA_UTILITARIOS / "figuras"
# ---------------------------------------------------------------------------


def resolver_metodo(m):
    if isinstance(m, str):
        chave = m.lower().strip()
        if chave not in METODOS_MAP:
            raise ValueError(f"Método '{m}' não reconhecido. Opções: {list(METODOS_MAP.keys())}")
        return METODOS_MAP[chave]
    return m


def executar(metodos=None, k=None, tf=None, x_lim_zoom=None, y_lim_zoom=None, pasta_saida=None, apenas_comparacao=False):
    """
    Executa a geração de gráficos de passo fixo para cada método e/ou a comparação conjunta.
    """
    configurar_estilo()
    prob = motivacao()
    if metodos is None:
        metodos = METODOS_PADRAO
    if k is None:
        k = K_PADRAO
    if tf is None:
        tf = TF_PADRAO
    if pasta_saida is None:
        pasta_saida = PASTA_FIG
    pasta_saida = Path(pasta_saida)

    metodos_funcs = [resolver_metodo(m) for m in metodos]

    print(f"=== Utilitário de Passo Fixo (k = {k:g}, TF = {tf:g}) ===")
    if x_lim_zoom is not None:
        print(f"-> Painel de zoom ativado: x = [{x_lim_zoom[0]:g}, {x_lim_zoom[1]:g}]", end="")
        if y_lim_zoom is not None:
            print(f", y = [{y_lim_zoom[0]:g}, {y_lim_zoom[1]:g}]")
        else:
            print()

    # 1. Gráficos individuais (se não foi solicitado apenas a comparação)
    if not apenas_comparacao or len(metodos_funcs) == 1:
        for m, m_func in zip(metodos, metodos_funcs):
            nome_str = getattr(m_func, "__name__", str(m))
            caminho_fig = pasta_saida / f"k_fixo_{nome_str}_k{str(k).replace('.', '_')}"
            plot_k_fixo(
                prob=prob,
                metodos=m_func,
                k=k,
                tf=tf,
                caminho=caminho_fig,
                x_lim_zoom=x_lim_zoom,
                y_lim_zoom=y_lim_zoom,
            )
            print(f"Salvo: {caminho_fig.with_suffix('.png')}")

    # 2. Gráfico comparativo conjunto com todos os métodos no mesmo eixo
    if len(metodos_funcs) > 1:
        nomes_curtos = "_".join(getattr(m, "__name__", str(m)).replace("euler_", "") for m in metodos_funcs)
        caminho_comp = pasta_saida / f"k_fixo_comparacao_{nomes_curtos}_k{str(k).replace('.', '_')}"
        plot_k_fixo(
            prob=prob,
            metodos=metodos_funcs,
            k=k,
            tf=tf,
            caminho=caminho_comp,
            x_lim_zoom=x_lim_zoom,
            y_lim_zoom=y_lim_zoom,
        )
        print(f"Salvo (Comparação conjunta): {caminho_comp.with_suffix('.png')}")


def main():
    parser = argparse.ArgumentParser(
        description="Utilitário para plotagem com passo fixo (k fixo) e zoom ajustável via plot_k_fixo."
    )
    parser.add_argument(
        "--metodos", "-m",
        nargs="+",
        default=METODOS_PADRAO,
        help=f"Métodos a executar. Opções: {list(METODOS_MAP.keys())}",
    )
    parser.add_argument(
        "--k", "-k",
        type=float,
        default=K_PADRAO,
        help=f"Passo de integração k (padrão: {K_PADRAO}).",
    )
    parser.add_argument(
        "--tf", "-t",
        type=float,
        default=TF_PADRAO,
        help=f"Instante final TF (padrão: {TF_PADRAO}).",
    )
    parser.add_argument(
        "--zoom", "-z",
        nargs=2,
        type=float,
        default=None,
        metavar=("T_MIN", "T_MAX"),
        help="Limites horizontais do painel de zoom (ex: --zoom 14.0 16.0).",
    )
    parser.add_argument(
        "--yzoom", "-yz",
        nargs=2,
        type=float,
        default=None,
        metavar=("Y_MIN", "Y_MAX"),
        help="Limites verticais do painel de zoom (ex: --yzoom -18.0 18.0).",
    )
    parser.add_argument(
        "--apenas-comparacao", "-cmp",
        action="store_true",
        help="Gera apenas o gráfico comparativo com os métodos juntos no mesmo gráfico.",
    )
    parser.add_argument(
        "--caminho", "-c",
        type=str,
        default=None,
        help="Caminho exato para salvar a figura (com ou sem .png).",
    )
    parser.add_argument(
        "--pasta",
        type=str,
        default=str(PASTA_FIG),
        help=f"Pasta de saída (padrão: {PASTA_FIG}).",
    )

    args = parser.parse_args()

    prob = motivacao()
    zoom_tuple = tuple(args.zoom) if args.zoom else None
    yzoom_tuple = tuple(args.yzoom) if args.yzoom else None

    if args.caminho is not None:
        metodos_funcs = [resolver_metodo(m) for m in args.metodos]
        plot_k_fixo(
            prob=prob,
            metodos=metodos_funcs,
            k=args.k,
            tf=args.tf,
            caminho=args.caminho,
            x_lim_zoom=zoom_tuple,
            y_lim_zoom=yzoom_tuple,
        )
        print(f"Gráfico salvo com sucesso em: {args.caminho}")
    else:
        executar(
            metodos=args.metodos,
            k=args.k,
            tf=args.tf,
            x_lim_zoom=zoom_tuple,
            y_lim_zoom=yzoom_tuple,
            pasta_saida=args.pasta,
            apenas_comparacao=args.apenas_comparacao,
        )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        executar()
