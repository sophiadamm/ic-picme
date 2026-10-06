
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import pendulo as pdl

def exec_p1():
    alpha = 0.7
    beta = 0.7
    T = 2 * math.pi
    m = 500
    h = T / (m + 1)
    t_i = np.linspace(h, T - h, m)
    t_tot = np.linspace(0, T, m + 2)

    chutes_info = {
        "24a": {
            "valores": 0.7*np.cos(t_i) + 0.5*np.sin(t_i),
            "texto": r"$\theta_0(t) = 0.7\cos(t) + 0.5\sin(t)$"
        },
        "24b": {
            "valores": 0.7 * np.ones(m),
            "texto": r"$\theta_0(t) = 0.7$"
        },
        "25": {
            "valores": 0.7 + np.sin(t_i/2),
            "texto": r"$\theta_0(t) = 0.7 + \sin(t/2)$"
        },
        "Customizado": {
            "valores": 0.7 + np.sin(t_i*4),
            "texto": r"$\theta_0(t) = 0.7 + \sin(4t)$"
        }
    }

    resultados = {}

    # --- Execução, Relatórios e Gráficos de Evolução ---
    for nome, info in chutes_info.items():
        chute = info["valores"]
        texto_func = info["texto"]
        
        theta_sol, hist_theta, hist_erro = pdl.newton(T, m, alpha, beta, chute)
        resultados[nome] = {
            'solucao': theta_sol,
            'chute': chute,
            'texto': texto_func
        }
        
        pdl.exibir_relatorio(nome, texto_func, hist_erro)
        pdl.plotar_evolucao_newton(t_tot, hist_theta, alpha, beta, nome, texto_func, f'graficos/evolucao_{nome}.png')

    # --- Grafico de COmparação das soluções ---
    plt.figure(figsize=(12, 7))
    cores = {'24a': 'blue', '24b': 'green', '25': 'red'}

    for nome, dados in resultados.items():
        theta_tot = np.concatenate(([alpha], dados['solucao'], [beta]))
        chute_tot = np.concatenate(([alpha], dados['chute'], [beta]))
        texto_funcao = dados['texto'] 
        
        if nome == "Customizado":
            plt.plot(t_tot, theta_tot, color='purple', linewidth=3, label='Solução Customizada')
            plt.plot(t_tot, chute_tot, color='purple', linewidth=2, linestyle=':', alpha=0.8, label=f'Chute: {texto_funcao}')
        else:
            plt.plot(t_tot, theta_tot, color=cores[nome], linewidth=1.5, alpha=0.6, label=f'Solução {nome}')
            plt.plot(t_tot, chute_tot, color=cores[nome], linewidth=1, linestyle='--', alpha=0.3, label=f'Chute {nome}: {texto_funcao}')

    plt.title('Comparação de Diferentes Chutes Iniciais no Pêndulo Não Linear')
    plt.xlabel('Tempo t')
    plt.ylabel('Ângulo θ(t)')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small') 
    plt.grid(True, alpha=0.4)
    plt.tight_layout()

    plt.savefig('graficos/comparacao_pendulo_destaque.png', dpi=300, bbox_inches='tight')
    plt.close()

# =============================================================================
# PARTE 2
# =============================================================================
def exec_p2():
    raise NotImplemented

if __name__ == "__main__":
    exec_p1()
    #exec_p2()