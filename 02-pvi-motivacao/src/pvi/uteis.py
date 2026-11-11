import matplotlib
matplotlib.use("Agg") 
import numpy as np
from pvi.problemas import g
import os



def erro_max(prob, t, U):
    return np.max(np.abs(U - prob.solucao(t)))

def resolver(metodo, prob, k, TF):
    """Roda o método e devolve (t, U, stats)."""
    n = round((TF - prob.t0) / k)
    t, U, stats = metodo(prob, n, k)
    return t, U, stats

def tabela_passo_a_passo(prob, nome, k, t_vals, U_vals, export_tex=True, export_csv=True, pasta_tab=None, pasta_dados=None):
    """Gera uma tabela detalhada com a trajetória e o erro em cada passo i."""
    
    # Se nenhuma opção foi escolhida, não faz sentido rodar
    if not (export_tex or export_csv):
        return
        
    nome_arquivo = f"trajetoria_{nome.lower().replace(' ', '_')}_k{str(k).replace('.', '')}"
    
    # Calcula a solução exata para todos os pontos
    solucao_vals = prob.solucao(t_vals)  
    erros = np.abs(U_vals - solucao_vals)
    
    # 1. Exportação LaTeX
    if export_tex:
        dir_tex = pasta_tab or "resultados/item_a/tabelas"
        os.makedirs(dir_tex, exist_ok=True)
        caminho_tex = os.path.join(dir_tex, f"{nome_arquivo}.tex")
        
        with open(caminho_tex, "w", encoding="utf-8") as f:
            f.write("\\begin{table}[H]\n")
            f.write("    \\centering\n")
            f.write("    \\begin{tabular}{ccccc}\n")
            f.write("        \\hline\n")
            f.write("        $i$ & $t_i$ & Numérico ($U_i$) & Exato ($y(t_i)$) & Erro ($|U_i - y(t_i)|$) \\\\\n")
            f.write("        \\hline\n")
            for i in range(len(t_vals)):
                f.write(f"        {i} & {t_vals[i]:.4f} & {U_vals[i]:.6f} & {solucao_vals[i]:.6f} & {erros[i]:.3e} \\\\\n")
            f.write("        \\hline\n")
            f.write("    \\end{tabular}\n")
            f.write(f"    \\caption{{Evolução passo a passo para o método {nome} com passo $k={k}$.}}\n")
            f.write(f"    \\label{{tab:{nome_arquivo}}}\n")
            f.write("\\end{table}\n")
        
    # 2. Exportação CSV
    if export_csv:
        dir_csv = pasta_dados or "resultados/item_a/dados"
        os.makedirs(dir_csv, exist_ok=True)
        caminho_csv = os.path.join(dir_csv, f"{nome_arquivo}.csv")
        
        with open(caminho_csv, "w", encoding="utf-8") as f:
            f.write("i,t_i,U_i,y_exato,erro_abs\n")
            for i in range(len(t_vals)):
                # Usa mais casas decimais no CSV para não perder precisão nos dados
                f.write(f"{i},{t_vals[i]:.4f},{U_vals[i]:.10f},{solucao_vals[i]:.10f},{erros[i]:.10e}\n")

def tabela_erros(prob, nome, solucoes, K, pasta_tab=None, pasta_dados=None):
    """Calcula erros, imprime no console e exporta para LaTeX e CSV com estatísticas completas."""

    dir_tex = pasta_tab or "resultados/item_a/tabelas"
    dir_csv = pasta_dados or "resultados/item_a/dados"
    os.makedirs(dir_tex, exist_ok=True)
    os.makedirs(dir_csv, exist_ok=True)
    
    nome_arquivo = nome.lower().replace(" ", "_").replace("ç", "c").replace("ã", "a")
    caminho_tex = os.path.join(dir_tex, f"erros_{nome_arquivo}.tex")
    caminho_csv = os.path.join(dir_csv, f"erros_{nome_arquivo}.csv")
    
    print(f"\n--- {nome} ---")
    print(f"{'k':>8} | {'passos':>6} | {'NFEV':>6} | {'CPU(ms)':>8} | {'erro máx':>12} | {'ordem obs.':>10}")
    print("-" * 81)
    
    erros = [erro_max(prob, t, U) for t, U, _ in solucoes]
    linhas_tabela = []
    
    for i, (k, (t, _, stats), e) in enumerate(zip(K, solucoes, erros)):
        ordem_num = np.log2(erros[i - 1] / e) if i > 0 else np.nan
        ordem_str = f"{ordem_num:10.2f}" if i > 0 else f"{'-':>10}"
        ordem_tex = f"{ordem_num:.2f}" if i > 0 else "-"
        
        # Converte runtime para milissegundos
        cpu_ms = stats['runtime'] * 1000
        
        
        print(f"{k:>8} | {len(t) - 1:>6} | {stats['nfev']:>6} | {cpu_ms:>8.2f} | {e:>12.3e} | {ordem_str}")
        
        linhas_tabela.append({
            'k': k, 'passos': len(t) - 1, 'nfev': stats['nfev'], 
            'cpu_ms': cpu_ms, 
            'erro': e, 'ordem': ordem_tex
        })

    # Exportação LaTeX
    with open(caminho_tex, "w", encoding="utf-8") as f:
        f.write("\\begin{table}[H]\n")
        f.write("    \\centering\n")
        f.write("    \\begin{tabular}{ccccccc}\n")
        f.write("        \\hline\n")
        f.write("        $k$ & Passos & NFEV & Tempo CPU (ms) & Erro Máximo & Ordem Observada \\\\\n")
        f.write("        \\hline\n")
        for linha in linhas_tabela:
            f.write(f"        {linha['k']} & {linha['passos']} & {linha['nfev']} & {linha['cpu_ms']:.2f}  & {linha['erro']:.3e} & {linha['ordem']} \\\\\n")
        f.write("        \\hline\n")
        f.write("    \\end{tabular}\n")
        f.write(f"    \\caption{{Análise computacional completa para o método {nome}.}}\n")
        f.write(f"    \\label{{tab:erros_{nome_arquivo}}}\n")
        f.write("\\end{table}\n")

    # CSV
    with open(caminho_csv, "w", encoding="utf-8") as f:
        f.write("k,passos,nfev,cpu_ms,erro_max,ordem\n")
        for linha in linhas_tabela:
            f.write(f"{linha['k']},{linha['passos']},{linha['nfev']},{linha['cpu_ms']:.4f},{linha['erro']:.10e},{linha['ordem']}\n")

def busca_passo_critico_euler(prob, tspan=(0.0, 1.6), n_inicial=1, n_max=5000, g_func=None):
    """
    Realiza uma busca numérica pelo menor número de passos n (ou maior passo k = (tf - t0)/n)
    em malhas uniformes que permite ao método de Euler recuado completar o intervalo tspan
    sem que o discriminante Delta_n = 1 - 4k*c_n se torne negativo (perda de raízes reais).
    """
    t0, tf = tspan
    h_total = tf - t0

    if g_func is None:
        from pvi.problemas import g as g_func

    historico_falhas = {}

    for n in range(n_inicial, n_max + 1):
        k = h_total / n
        u = prob.y0
        completou = True
        delta_min_n = float("inf")

        for step in range(n):
            tn1 = t0 + (step + 1) * k
            c = u - k * g_func(tn1)
            delta = 1.0 - 4.0 * k * c

            if delta < delta_min_n:
                delta_min_n = delta

            if delta < 0:
                completou = False
                historico_falhas[n] = {
                    "k": k,
                    "passo_falha": step + 1,
                    "t_falha": tn1,
                    "delta": delta,
                }
                break

            # Avanço para a menor raiz real (ramo físico)
            u = (1.0 - delta**0.5) / (2.0 * k)

        if completou:
            return {
                "n_critico": n,
                "k_critico": k,
                "delta_min": delta_min_n,
                "historico_falhas": historico_falhas,
            }

    return {
        "n_critico": None,
        "k_critico": None,
        "delta_min": None,
        "historico_falhas": historico_falhas,
    }


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


def exportar_tabela_discriminante(
    prob,
    k=0.2,
    n_passos=3,
    g_func=None,
    export_tex=True,
    export_csv=True,
    pasta_tab=None,
    pasta_dados=None,
    caminho_tab=None,
):
    """
    Gera a tabela analítica (LaTeX e opcionalmente CSV) acompanhando passo a passo
    a evolução do discriminante Delta_n = 1 - 4k c_n no método de Euler recuado,
    comparando os valores teóricos sobre a curva exata com a trajetória simulada.
    """
    if g_func is None:
        g_func = g

    nome_sufixo = f"k{str(k).replace('.', '')}"
    nome_arquivo = f"discriminante_euler_{nome_sufixo}"

    dir_tex = pasta_tab or "resultados/item_a/tabelas"
    dir_csv = pasta_dados or "resultados/item_a/dados"

    linhas = []
    linhas_dados = []
    u = prob.y0
    passo_falha = None
    c_falha = None

    for step in range(n_passos):
        tn = prob.t0 + step * k
        tn1 = tn + k
        c_num = u - k * g_func(tn1)
        delta_num = 1.0 - 4.0 * k * c_num
        c_exato = prob.solucao(tn) - k * g_func(tn1)
        delta_exato = 1.0 - 4.0 * k * c_exato

        d_num_str = f"\\mathbf{{{delta_num:+.6f}}}" if delta_num < 0 else f"{delta_num:+.6f}"
        linhas.append(
            f"        ${step} \\to {step+1}$ & ${tn:.1f} \\to {tn1:.1f}$ & "
            f"${prob.solucao(tn):.6f}$ & ${u:.6f}$ & "
            f"${c_exato:.6f}$ & ${c_num:.6f}$ & "
            f"${delta_exato:+.6f}$ & ${d_num_str}$ \\\\"
        )
        linhas_dados.append({
            "passo": f"{step}->{step+1}",
            "tn": tn,
            "tn1": tn1,
            "y_exato": prob.solucao(tn),
            "u_num": u,
            "c_exato": c_exato,
            "c_num": c_num,
            "delta_exato": delta_exato,
            "delta_num": delta_num,
        })

        if delta_num < 0:
            passo_falha = (step, step + 1, tn1)
            c_falha = c_num
            break

        u = (1.0 - delta_num**0.5) / (2.0 * k)

    c_crit = 1.0 / (4.0 * k)
    if passo_falha:
        s_de, s_para, t_f = passo_falha
        texto_falha = (
            f"No passo ${s_de} \\to {s_para}$ ($t_{{n+1}} = {t_f:.1f}$), a barreira crítica "
            f"$c_n \\le \\frac{{1}}{{4k}} = {c_crit:.2f}$ é violada ($c_{s_de}^{{\\text{{num}}}} \\approx {c_falha:.4f}$), "
            f"tornando $\\Delta_{s_de}^{{\\text{{num}}}} < 0$ e impossibilitando a existência de qualquer raiz real."
        )
    else:
        texto_falha = (
            f"O discriminante numérico $\\Delta_n^{{\\text{{num}}}}$ permaneceu não-negativo em todos os passos calculados."
        )

    conteudo_tex = (
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
        f"{texto_falha}}}\n"
        f"    \\label{{tab:{nome_arquivo}}}\n"
        "\\end{table}\n"
    )

    if export_tex:
        if caminho_tab:
            caminho_tex = caminho_tab
            os.makedirs(os.path.dirname(caminho_tex) or ".", exist_ok=True)
        else:
            os.makedirs(dir_tex, exist_ok=True)
            caminho_tex = os.path.join(dir_tex, f"{nome_arquivo}.tex")

        with open(caminho_tex, "w", encoding="utf-8") as f:
            f.write(conteudo_tex)
        print(f"Tabela de discriminante salva em: {caminho_tex}")

    if export_csv:
        os.makedirs(dir_csv, exist_ok=True)
        caminho_csv = os.path.join(dir_csv, f"{nome_arquivo}.csv")
        with open(caminho_csv, "w", encoding="utf-8") as f:
            f.write("passo,tn,tn1,y_exato,u_num,c_exato,c_num,delta_exato,delta_num\n")
            for d in linhas_dados:
                f.write(
                    f"{d['passo']},{d['tn']:.4f},{d['tn1']:.4f},{d['y_exato']:.10f},"
                    f"{d['u_num']:.10f},{d['c_exato']:.10f},{d['c_num']:.10f},"
                    f"{d['delta_exato']:.10f},{d['delta_num']:.10f}\n"
                )

    return linhas_dados


# Alias para retrocompatibilidade
exportar_tabela_discriminante_tex = exportar_tabela_discriminante
