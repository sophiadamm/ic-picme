import sys
import os
from pathlib import Path

# Garante que o Python encontre a pasta 'src' ao rodar de 'experimentos/' ou da raiz
DIR_ATUAL = Path(__file__).resolve().parent
sys.path.append(str((DIR_ATUAL / ".." / "src").resolve()))

from pvi.problemas import motivacao
from pvi.uteis import busca_passo_critico_euler

def testar():
    prob = motivacao()

    print("=" * 70)
    print("BUSCA NUMÉRICA DE PASSO CRÍTICO DO EULER IMPLÍCITO (Delta >= 0)")
    print("=" * 70)

    # 1. Teste no intervalo padrão [0, 1.6]
    print("\n[1] Intervalo padrão: [0, 1.6]")
    print("-" * 50)
    res_16 = busca_passo_critico_euler(prob, tspan=(0.0, 1.6), n_inicial=1, n_max=100)
    n16 = res_16["n_critico"]
    k16 = res_16["k_critico"]
    d16 = res_16["delta_min"]
    
    print(f"Menor número de passos viável: n = {n16}")
    print(f"Maior passo uniforme:          k = {k16:.6f}  (~ 1.6/{n16})")
    print(f"Discriminante mínimo:          Delta_min = {d16:.4f} > 0 (sucesso!)")

    # 2. Teste no intervalo estendido [0, 5.0]
    print("\n" + "=" * 70)
    print("[2] Intervalo estendido: [0, 5.0]")
    print("-" * 50)
    # n=1 salta toda a dinâmica intermediária, então iniciamos em n=2
    res_5 = busca_passo_critico_euler(prob, tspan=(0.0, 5.0), n_inicial=2, n_max=2000)
    n5 = res_5["n_critico"]
    k5 = res_5["k_critico"]
    d5 = res_5["delta_min"]

    print(f"Menor número de passos viável: n = {n5}")
    print(f"Maior passo uniforme:          k = {k5:.6f}  (~ 5.0/{n5})")
    print(f"Discriminante mínimo:          Delta_min = {d5:.4f} > 0 (sucesso!)")


if __name__ == "__main__":
    testar()

