import matplotlib
matplotlib.use("Agg") 
import numpy as np
from pvi.problemas import motivacao
from pvi.metodos import euler_explicito, euler_implicito
from pvi.plotagem import configurar_estilo, plot_comparacao, plot_fig122
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

