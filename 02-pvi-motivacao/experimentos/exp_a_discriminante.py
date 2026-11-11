import sys
import os
from pathlib import Path

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = Path(__file__).resolve().parent
sys.path.append(str((DIR_ATUAL / ".." / "src").resolve()))

import matplotlib
matplotlib.use("Agg")

from pvi.problemas import motivacao, g
from pvi.plotagem import configurar_estilo, plot_discriminante_euler

# ----------------------------- parâmetros ---------------------------------
TF = 1.6
K = (0.2, 0.1, 0.05)
K2 = (0.0125, 0.00625, 0.003125, 0.0015625)
PASTA_ITEM = (DIR_ATUAL / ".." / "resultados" / "item_a").resolve()
PASTA_FIG = PASTA_ITEM / "figuras"
PASTA_TAB = PASTA_ITEM / "tabelas"
# ---------------------------------------------------------------------------

def exportar_tabela_discriminante_tex(prob, k=0.2, caminho_tab=None):
    """Gera a tabela LaTeX com os 3 passos de k=0.2 comparando o discriminante exato e simulado."""
    PASTA_TAB.mkdir(parents=True, exist_ok=True)
    caminho = caminho_tab or (PASTA_TAB / "discriminante_euler_k02.tex")
    
    linhas = []
    u = prob.y0
    for step in range(3):
        tn = prob.t0 + step * k
        tn1 = tn + k
        c_num = u - k * g(tn1)
        delta_num = 1.0 - 4.0 * k * c_num
        c_exato = prob.solucao(tn) - k * g(tn1)
        delta_exato = 1.0 - 4.0 * k * c_exato
        
        d_num_str = f"\\mathbf{{{delta_num:+.6f}}}" if delta_num < 0 else f"{delta_num:+.6f}"
        linhas.append(
            f"        ${step} \\to {step+1}$ & ${tn:.1f} \\to {tn1:.1f}$ & "
            f"${prob.solucao(tn):.6f}$ & ${u:.6f}$ & "
            f"${c_exato:.6f}$ & ${c_num:.6f}$ & "
            f"${delta_exato:+.6f}$ & ${d_num_str}$ \\\\"
        )
        if delta_num >= 0:
            u = (1.0 - delta_num**0.5) / (2.0 * k)
            
    conteudo = (
        "\\begin{table}[H]\n"
        "    \\centering\n"
        "    \\small\n"
        "    \\begin{tabular}{cccccccc}\n"
        "        \\hline\n"
        "        Passo ($n \\to n+1$) & $t_n \\to t_{n+1}$ & $y(t_n)$ & $U_n$ & "
        "$c_n^{\\text{exato}}$ & $c_n^{\\text{num}}$ & $\\Delta_n^{\\text{exato}}$ & $\\Delta_n^{\\text{num}}$ \\\\\n"
        "        \\hline\n"
        + "\n".join(linhas) + "\n"
        "        \\hline\n"
        "    \\end{tabular}\n"
        f"    \\caption{{Evolução algébrica do discriminante $\\Delta_n = 1 - 4k c_n$ no método de Euler recuado com $k = {k}$. "
        f"No passo $2 \\to 3$ ($t_{{n+1}} = 0{{,}}6$), a barreira crítica $c_n \\le \\frac{{1}}{{4k}} = {1/(4*k):.2f}$ é violada "
        f"($c_2^{{\\text{{num}}}} \\approx 1{{,}}2532$), tornando $\\Delta_2^{{\\text{{num}}}} < 0$ e impossibilitando a existência de qualquer raiz real.}}\n"
        "    \\label{tab:discriminante_euler_k02}\n"
        "\\end{table}\n"
    )
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"Tabela de discriminante salva em: {caminho}")

def executar():
    configurar_estilo()
    prob = motivacao()

    # 1. Intervalo padrão [0, 1.6] — Passos clássicos K = (0.2, 0.1, 0.05) (1 painel)
    caminho_fig = PASTA_FIG / "a_discriminante_euler"
    plot_discriminante_euler(prob, K, TF, caminho_fig, g_func=g)

    # 2. Intervalo estendido [0, 5.0] — Passos clássicos K = (0.2, 0.1, 0.05) (1 painel)
    caminho_fig2 = PASTA_FIG / "a_discriminante_eulerT5"
    plot_discriminante_euler(prob, K, 5.0, caminho_fig2, g_func=g)

    # 3. Intervalo estendido [0, 5.0] — Malhas refinadas K2 (2 painéis: visão global + zoom)
    caminho_fig3 = PASTA_FIG / "a_discriminante_eulerT5_ref"
    plot_discriminante_euler(prob, K2, 5.0, caminho_fig3, g_func=g, x_lim_zoom=(3.8, 5.02))

    exportar_tabela_discriminante_tex(prob, k=0.2)

    k = 0.2
    u = prob.y0
    for step in range(3):
        tn = prob.t0 + step * k
        tn1 = tn + k
        c_num = u - k * g(tn1)
        delta_num = 1.0 - 4.0 * k * c_num
        c_exato = prob.solucao(tn) - k * g(tn1)
        delta_exato = 1.0 - 4.0 * k * c_exato

        print(f"Passo {step + 1} (t = {tn:.2f} -> {tn1:.2f}):")
        print(f"  Exato:     y(tn) = {prob.solucao(tn):.6f} | c = {c_exato:.6f} | Delta = {delta_exato:.6f}")
        print(f"  Simulado:  U_n   = {u:.6f} | c = {c_num:.6f} | Delta = {delta_num:.6f}")

        if delta_num < 0:
            print("  -> Delta < 0! Equação quadrática não possui raízes reais.")
            break
        u = (1.0 - delta_num**0.5) / (2.0 * k)

if __name__ == "__main__":
    executar()
