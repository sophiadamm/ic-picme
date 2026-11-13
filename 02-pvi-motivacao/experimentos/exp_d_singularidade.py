import os
import sys

# Garante que o Python encontre a pasta 'src' ao rodar o script de dentro de 'experimentos/'
DIR_ATUAL = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR_ATUAL, '..', 'src')))

import matplotlib
matplotlib.use("Agg")
import numpy as np

from pvi.problemas import motivacao
from pvi.metodos import euler_explicito, euler_implicito, rk4, adams_moulton
from pvi.plotagem import configurar_estilo, plot_singularidade
from pvi.uteis import resolver, tabela_singularidade

# =============================================================================
# 1. PARÂMETROS (edite aqui)
# =============================================================================
POLO = -1.0
LIMITE_EXPLOSAO = 1e6     # |U| acima disso = explosão; é também o limite do eixo y
LINTHRESH = 10.0          # faixa linear do eixo symlog: |y| <= LINTHRESH

INTERVALOS = {
    # limites: intervalo de integração | xlim: janela exibida
    "m2_2": {"limites": (-2.0, 2.0), "xlim": (-2.0, 2.0), "tex": r"$[-2,\, 2]$"},
    # Em [-5, 40] tudo o que envolve o polo acontece em t < 0; o comportamento em
    # [0, 40] (instabilidade de longo prazo) é o objeto do exp_d.py.
    "m5_40": {"limites": (-5.0, 40.0), "xlim": (-5.0, 3.0), "tex": r"$[-5,\, 40]$"},
}

# Passo k de cada cenário. Para "cai no polo", k deve dividir a distância de a até -1
# (1 e 4); para "pula o polo", não deve (ex.: 0.07, 0.03, 0.3).
CENARIOS = {
    "sd_cai_polo": {
        "k": 0.1,
        "descricao": "sem decomposição, malha cai no polo",
    },
    "sd_pula_polo": {
        "k": 0.07,
        "descricao": "sem decomposição, malha pula o polo",
    },
    "cd": {
        "k": 0.1,
        "descricao": "com decomposição de ramos",
    },
    "cd_k07": {
        "k": 0.07,
        "descricao": "com decomposição de ramos",
    },
}

METODOS = {
    "Euler explícito": euler_explicito,
    "Euler implícito": euler_implicito,
    "RK4": rk4,
    "Adams-Moulton 2": adams_moulton,
}

COR_DIRETA, COR_ESQ, COR_DIR = "#d62728", "#1f77b4", "#2ca02c"

PASTA_ITEM = os.path.abspath(os.path.join(DIR_ATUAL, '..', 'resultados', 'item_d'))
PASTA_FIG = os.path.join(PASTA_ITEM, 'figuras')
PASTA_TAB = os.path.join(PASTA_ITEM, 'tabelas')
PASTA_DADOS = os.path.join(PASTA_ITEM, 'dados')


# =============================================================================
# 2. SIMULAÇÕES
# =============================================================================
def simular_sd(a, b, k):
    """Integra direto de a até b partindo de y(a) = y_exata(a), sem parar no polo."""
    prob = motivacao(t0=a, limite_explosao=LIMITE_EXPLOSAO, parar_na_singularidade=False)
    paineis = {}
    for nome, metodo in METODOS.items():
        paineis[nome] = [{
            "metodo": nome, "ramo": "", "prob": prob, "k": k, "tf": b,
            "sol": resolver(metodo, prob, k, b),
            "cor": COR_DIRETA, "marker": "o",
            "label": f"numérica a partir de $y({a:g})$ ($k = {k:g}$)",
        }]
    return paineis


def simular_cd(a, b, k):
    """Ramo esquerdo: y(a) -> b. Ramo direito: y(0) = 2 -> a e -> b. Para antes do polo."""
    prob_esq = motivacao(t0=a, limite_explosao=LIMITE_EXPLOSAO)
    prob_dir = motivacao(limite_explosao=LIMITE_EXPLOSAO)
    trechos = [  # (ramo, PVI, instante final, cor, marcador, legenda)
        ("esq.", prob_esq, b, COR_ESQ, "s", f"ramo esquerdo, $y({a:g})$ ($k = {k:g}$)"),
        ("dir. (trás)", prob_dir, a, COR_DIR, "^", f"ramo direito, $y(0) = 2$ ($k = {k:g}$)"),
        ("dir. (frente)", prob_dir, b, COR_DIR, "^", None),
    ]
    paineis = {}
    for nome, metodo in METODOS.items():
        paineis[nome] = [{
            "metodo": nome, "ramo": ramo, "prob": prob, "tf": tf,
            "k": k if tf >= prob.t0 else -k,
            "sol": resolver(metodo, prob, k, tf),
            "cor": cor, "marker": marc, "label": lbl,
        } for ramo, prob, tf, cor, marc, lbl in trechos]
    return paineis


# =============================================================================
# 3. EXECUÇÃO
# =============================================================================
def executar():
    configurar_estilo()
    prob_ref = motivacao()

    for sufixo, cfg in INTERVALOS.items():
        a, b = cfg["limites"]
        for cen_id, cen in CENARIOS.items():
            k = cen["k"]
            print(f"\n=== Intervalo [{a:g}, {b:g}] | {cen['descricao']} | k = {k} ===")
            decomp = cen_id.startswith("cd")
            with np.errstate(all="ignore"):
                paineis = (simular_cd if decomp else simular_sd)(a, b, k)

            plot_singularidade(
                prob_ref, paineis, (a, b),
                f"{PASTA_FIG}/d_{sufixo}_{cen_id}",
                f"PVI de motivação em {cfg['tex']}: {cen['descricao']} ($k = {k:g}$)",
                xlim=cfg["xlim"], ylim=(-LIMITE_EXPLOSAO, LIMITE_EXPLOSAO),
                linthresh=LINTHRESH, polo=POLO,
                ramo_proprio="ambos" if decomp else "esq",
            )

            casos = [c for lista in paineis.values() for c in lista]
            for c in casos:
                c["ramo"] = c["ramo"] or "direto"
            tabela_singularidade(
                casos, f"{sufixo}_{cen_id}",
                f"Integração do PVI de motivação em {cfg['tex']}: {cen['descricao']} ($k = {k:g}$).",
                pasta_tab=PASTA_TAB, pasta_dados=PASTA_DADOS,
            )

    print("\nExperimento D (singularidade) concluído com sucesso!")


if __name__ == "__main__":
    executar()
