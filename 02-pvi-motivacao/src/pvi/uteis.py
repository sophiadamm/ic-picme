import matplotlib
matplotlib.use("Agg") 
import numpy as np
from pvi.problemas import g
from pvi.metodos import rk4
import os

def erro_max(prob, t, U):
    return np.max(np.abs(U - prob.solucao(t)))

def resolver(metodo, prob, k, TF):
    """Roda o método e devolve (t, U, stats).

    O sentido da integração é dado por TF: se TF < t0 o passo é tomado negativo
    (integração para trás), qualquer que seja o sinal de k informado.
    """
    k = abs(k) if TF >= prob.t0 else -abs(k)
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

#--------------------------------------------------------------------------------------------------------------------------------

import numpy as np
import os
from pvi.metodos import rk4
from pvi.problemas import g

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


def calcular_evolucao_discriminante(prob, k, n_passos, metodo="euler", g_func=None):
    """
    Motor matemático central. Retorna a evolução passo a passo do discriminante
    sem se preocupar com formatação, arquivos ou gráficos.
    """
    if g_func is None:
        g_func = g

    is_am = metodo if isinstance(metodo, bool) else (str(metodo).lower() in ("adams_moulton", "adams_moulton_2", "am2", "am"))
    n_passos = int(round(n_passos))
    passos_iniciais = 2 if is_am else 1
    a = (5.0 * k / 12.0) if is_am else k

    # Funções auxiliares para cálculo do 'c' dependendo do método
    def calc_c_euler(t_h, u_h, tn1):
        return u_h[-1] - k * g_func(tn1)
        
    def calc_c_am2(t_h, u_h, tn1):
        fn = prob.f(t_h[-1], u_h[-1])
        fn_m1 = prob.f(t_h[-2], u_h[-2])
        return u_h[-1] + (k / 12.0) * (8.0 * fn - fn_m1 - 5.0 * g_func(tn1))
        
    calc_c = calc_c_am2 if is_am else calc_c_euler
    
    # Inicialização
    t_hist = [prob.t0 + i * k for i in range(passos_iniciais)]
    dados = []
    
    if passos_iniciais == 1:
        u_hist = [prob.y0]
    else:
        _, u_init, _ = rk4(prob, passos_iniciais - 1, k)
        u_hist = list(u_init)
        for i in range(passos_iniciais - 1):
            dados.append({
                "passo": f"{i}->{i+1}", "tn": t_hist[i], "tn1": t_hist[i+1],
                "y_exato": prob.solucao(t_hist[i]), "u_num": u_hist[i],
                "c_exato": np.nan, "c_num": np.nan, "delta_exato": np.nan, "delta_num": np.nan
            })

    # Laço principal via Bhaskara
    for step in range(passos_iniciais - 1, n_passos):
        tn1 = prob.t0 + (step + 1) * k
        
        c_num = calc_c(t_hist, u_hist, tn1)
        delta_num = 1.0 - 4.0 * a * c_num
        
        u_exato_hist = [prob.solucao(t) for t in t_hist]
        c_exato = calc_c(t_hist, u_exato_hist, tn1)
        delta_exato = 1.0 - 4.0 * a * c_exato

        dados.append({
            "passo": f"{step}->{step+1}", "tn": t_hist[-1], "tn1": tn1,
            "y_exato": prob.solucao(t_hist[-1]), "u_num": u_hist[-1],
            "c_exato": c_exato, "c_num": c_num, "delta_exato": delta_exato, "delta_num": delta_num
        })

        if delta_num < 0:
            break

        un1 = (1.0 - delta_num**0.5) / (2.0 * a)
        t_hist.append(tn1)
        u_hist.append(un1)

    return dados, a, is_am


def _passo_critico(prob, tspan=(0.0, 1.6), n_inicial=1, n_max=5000, metodo="euler", g_func=None):
    """
    Busca o menor número de passos (n) onde o método implícito sobrevive ao intervalo
    tspan sem que o discriminante fique negativo, consumindo o motor matemático central.
    """
    t0, tf = tspan
    h_total = tf - t0

    if g_func is None:
        g_func = g

    historico_falhas = {}

    for n in range(n_inicial, n_max + 1):
        k = h_total / n
        
        # 1. Delega todo o trabalho pesado para o motor matemático
        dados, _, _ = calcular_evolucao_discriminante(prob, k, n, metodo, g_func)
        
        # 2. Avaliamos o último passo calculado
        ultimo_passo = dados[-1]
        
        # Proteção: Ignora partições tão grossas que sequer saíram da inicialização (RK4)
        if np.isnan(ultimo_passo['delta_num']):
            continue
            
        # 3. Verifica se houve falha (delta_num < 0)
        if ultimo_passo['delta_num'] < 0:
            historico_falhas[n] = {
                "t_falha": ultimo_passo['tn1'],
                "delta": ultimo_passo['delta_num']
            }
        else:
            # Coleta o delta_min ignorando as linhas de inicialização (NaN)
            delta_min = min(d['delta_num'] for d in dados if not np.isnan(d['delta_num']))
            
            return {
                "n_critico": n,
                "k_critico": k,
                "delta_min": delta_min,
                "historico_falhas": historico_falhas,
            }

    # Se esgotou o n_max e não convergiu
    return {
        "n_critico": None,
        "k_critico": None,
        "delta_min": None,
        "historico_falhas": historico_falhas,
    }


def busca_critica(prob, metodo='euler', tspan=(0.0, 1.6)):
    print("=" * 70)
    print(f"BUSCA NUMÉRICA DE PASSO CRÍTICO: {metodo.upper()} IMPLÍCITO (Delta >= 0)")
    print("=" * 70)

    # Desempacota o intervalo para formatar direito
    t0, tf = tspan
    h_total = tf - t0

    print(f"\nIntervalo : [{t0}, {tf}]")
    print("-" * 50)
    
    # Chama a função usando a variável tspan dinâmica e um n_max seguro
    res = _passo_critico(prob, tspan=tspan, n_inicial=1, n_max=5000, metodo=metodo)
    
    n = res["n_critico"]
    k = res["k_critico"]
    d = res["delta_min"]

    # Proteção caso o método não convirja dentro do n_max
    if n is not None:
        print(f"Menor número de passos viável: n = {n}")
        print(f"Maior passo uniforme:          k = {k:.6f}  (~ {h_total:g}/{n})")
        print(f"Discriminante mínimo:          Delta_min = {d:.4f} > 0 (sucesso!)\n")
    else:
        print(f"FALHA: Não foi possível encontrar um passo viável no limite testado.\n")


def exportar_tabela_discriminante(
    prob, k=0.2, n_passos=3, metodo="euler", g_func=None,
    export_tex=True, export_csv=True, pasta_tab=None, pasta_dados=None
):
    """
    Função de View: Formata os dados do discriminante e salva os arquivos LaTeX/CSV.
    """
    dados, a, is_am = calcular_evolucao_discriminante(prob, k, n_passos, metodo, g_func)
    
    simb_c = "\\tilde{c}_n" if is_am else "c_n"
    nome_tex = "Adams-Moulton de 2 passos" if is_am else "Euler recuado"
    c_crit = 1.0 / (4.0 * a)
    nome_arquivo = f"discriminante_{metodo.lower()}_k{str(k).replace('.','')}"
    
    linhas = []
    for d in dados:
        if np.isnan(d['delta_num']):
            linhas.append(
                f"        ${d['passo']}$ & ${d['tn']:.1f} \\to {d['tn1']:.1f}$ & "
                f"${d['y_exato']:.6f}$ & ${d['u_num']:.6f}$ & \\text{{(RK4)}} & "
                f"\\text{{(RK4)}} & \\text{{---}} & \\text{{---}} \\\\"
            )
        else:
            d_str = f"\\mathbf{{{d['delta_num']:+.6f}}}" if d['delta_num'] < 0 else f"{d['delta_num']:+.6f}"
            linhas.append(
                f"        ${d['passo']}$ & ${d['tn']:.1f} \\to {d['tn1']:.1f}$ & "
                f"${d['y_exato']:.6f}$ & ${d['u_num']:.6f}$ & ${d['c_exato']:.6f}$ & "
                f"${d['c_num']:.6f}$ & ${d['delta_exato']:+.6f}$ & ${d_str}$ \\\\"
            )

    # Verifica o último passo processado para montar o texto de falha
    ultimo = dados[-1]
    if not np.isnan(ultimo['delta_num']) and ultimo['delta_num'] < 0:
        texto_falha = f"No passo ${ultimo['passo']}$ ($t_{{n+1}} = {ultimo['tn1']:.1f}$), a barreira ${simb_c} \\le {c_crit:.2f}$ é violada, tornando $\\Delta < 0$."
    else:
        texto_falha = "O discriminante numérico permaneceu positivo ($\\Delta > 0$), preservando raízes reais."

    # Exportação LaTeX
    if export_tex:
        dir_tex = pasta_tab or ("resultados/item_c/tabelas" if is_am else "resultados/item_a/tabelas")
        os.makedirs(dir_tex, exist_ok=True)
        caminho_tex = os.path.join(dir_tex, f"{nome_arquivo}.tex")
        
        eq_delta = f"\\Delta_n = 1 - 4({a:.3f}){simb_c}"
        tex_content = (
            "\\begin{table}[H]\n    \\centering\n    \\small\n    \\begin{tabular}{cccccccc}\n        \\hline\n"
            f"        Passo & $t_n \\to t_{{n+1}}$ & $y(t_n)$ & $U_n$ & ${simb_c}^{{\\text{{exato}}}}$ & "
            f"${simb_c}^{{\\text{{num}}}}$ & $\\Delta_n^{{\\text{{exato}}}}$ & $\\Delta_n^{{\\text{{num}}}}$ \\\\\n        \\hline\n"
            + "\n".join(linhas) + "\n        \\hline\n    \\end{tabular}\n"
            f"    \\caption{{Evolução do discriminante ${eq_delta}$ no método {nome_tex}. {texto_falha}}}\n"
            f"    \\label{{tab:{nome_arquivo}}}\n\\end{{table}}\n"
        )
        with open(caminho_tex, "w", encoding="utf-8") as f:
            f.write(tex_content)

    # Exportação CSV
    if export_csv:
        dir_csv = pasta_dados or ("resultados/item_c/dados" if is_am else "resultados/item_a/dados")
        os.makedirs(dir_csv, exist_ok=True)
        caminho_csv = os.path.join(dir_csv, f"{nome_arquivo}.csv")
        
        with open(caminho_csv, "w", encoding="utf-8") as f:
            f.write("passo,tn,tn1,y_exato,u_num,c_exato,c_num,delta_exato,delta_num\n")
            for d in dados:
                # Tratamento de segurança para não escrever NaN como string formatada em float
                c_ex = f"{d['c_exato']:.10f}" if not np.isnan(d['c_exato']) else "NaN"
                c_num = f"{d['c_num']:.10f}" if not np.isnan(d['c_num']) else "NaN"
                d_ex = f"{d['delta_exato']:.10f}" if not np.isnan(d['delta_exato']) else "NaN"
                d_num = f"{d['delta_num']:.10f}" if not np.isnan(d['delta_num']) else "NaN"
                
                f.write(
                    f"{d['passo']},{d['tn']:.4f},{d['tn1']:.4f},{d['y_exato']:.10f},"
                    f"{d['u_num']:.10f},{c_ex},{c_num},{d_ex},{d_num}\n"
                )
                
    return dados


# Alias para retrocompatibilidade
exportar_tabela_discriminante_tex = exportar_tabela_discriminante



# --------------------------------------------------------------------------------------------------------------------------------
# Item d: integração em intervalos que contêm a singularidade t = -1
# --------------------------------------------------------------------------------------------------------------------------------

MOTIVOS_PARADA = {
    'concluido': 'concluído',
    'explosao': 'explosão',
    'newton': 'Newton não convergiu',
    'singularidade': 'parou antes do polo',
}


def tabela_singularidade(casos, nome_arquivo, legenda, pasta_tab=None, pasta_dados=None):
    """Tabela-resumo de integrações que podem parar antes do instante final.

    `casos` é uma lista de dicionários com as chaves:
        'metodo', 'ramo', 'prob', 'k', 'tf' (instante final pedido) e 'sol' = (t, U, stats).

    Para cada caso registra onde a integração parou e por quê, além do erro no último
    ponto aceito e do erro máximo no trecho efetivamente percorrido. Exporta .tex e .csv.
    """
    dir_tex = pasta_tab or "resultados/item_d/tabelas"
    dir_csv = pasta_dados or "resultados/item_d/dados"
    os.makedirs(dir_tex, exist_ok=True)
    os.makedirs(dir_csv, exist_ok=True)

    linhas = []
    print(f"\n--- {legenda} ---")
    print(f"{'método':<24} | {'ramo':<16} | {'k':>7} | {'t pedido':>8} | {'t parada':>8} | "
          f"{'passos':>6} | {'U final':>11} | {'y exato':>11} | {'erro final':>10} | motivo")
    print("-" * 140)
    for c in casos:
        t, U, stats = c['sol']
        prob = c['prob']
        y_ex = prob.solucao(t)
        erros = np.abs(U - y_ex)
        motivo = MOTIVOS_PARADA.get(stats.get('motivo', ''), stats.get('motivo', '-'))
        if stats.get('cruzamentos'):
            motivo += " (atravessou t = -1)"
        linha = {
            'metodo': c['metodo'], 'ramo': c['ramo'], 'k': c['k'], 'tf': c['tf'],
            't_parada': t[-1], 'passos': len(t) - 1, 'U_final': U[-1], 'y_final': y_ex[-1],
            'erro_final': erros[-1], 'erro_max': np.max(erros), 'nfev': stats['nfev'],
            'motivo': motivo,
        }
        linhas.append(linha)
        print(f"{linha['metodo']:<24} | {linha['ramo']:<16} | {linha['k']:>7} | {linha['tf']:>8g} | "
              f"{linha['t_parada']:>8.3f} | {linha['passos']:>6} | {linha['U_final']:>11.4e} | "
              f"{linha['y_final']:>11.4e} | {linha['erro_final']:>10.3e} | {motivo}")

    with open(os.path.join(dir_tex, f"{nome_arquivo}.tex"), "w", encoding="utf-8") as f:
        f.write("\\begin{table}[H]\n")
        f.write("    \\centering\n")
        f.write("    \\small\n")
        f.write("    \\begin{tabular}{llcccccl}\n")
        f.write("        \\hline\n")
        f.write("        Método & Ramo & $k$ & $t$ pedido & $t$ de parada & $U$ final & "
                "$y(t)$ exato & Motivo \\\\\n")
        f.write("        \\hline\n")
        for l in linhas:
            f.write(f"        {l['metodo']} & {l['ramo']} & {l['k']:g} & {l['tf']:g} & "
                    f"{l['t_parada']:.3f} & {l['U_final']:.3e} & {l['y_final']:.3e} & {l['motivo']} \\\\\n")
        f.write("        \\hline\n")
        f.write("    \\end{tabular}\n")
        f.write(f"    \\caption{{{legenda}}}\n")
        f.write(f"    \\label{{tab:{nome_arquivo}}}\n")
        f.write("\\end{table}\n")

    with open(os.path.join(dir_csv, f"{nome_arquivo}.csv"), "w", encoding="utf-8") as f:
        f.write("metodo,ramo,k,t_pedido,t_parada,passos,nfev,U_final,y_exato,erro_final,erro_max,motivo\n")
        for l in linhas:
            f.write(f"{l['metodo']},{l['ramo']},{l['k']},{l['tf']},{l['t_parada']:.6f},{l['passos']},"
                    f"{l['nfev']},{l['U_final']:.10e},{l['y_final']:.10e},{l['erro_final']:.10e},"
                    f"{l['erro_max']:.10e},{l['motivo']}\n")

    return linhas
