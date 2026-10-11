
import numpy as np
import matplotlib.pyplot as plt
import math
import pendulo as pdl

# =============================================================================
# PARTE 1
# =============================================================================

def plotar_comparacao(t_tot, resultados, alpha, beta, filename):
    """Versão original: tudo em um único gráfico, com transparência."""
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
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()


def plotar_comparacao_paineis(t_tot, resultados, alpha, beta, filename):
    """Versão nova: chutes (esq.) x soluções (dir.)"""
    cores = {
        '24a': '#0072B2',
        '24b': '#009E73',
        '25': '#D55E00',
        'Customizado': '#CC79A7'
    }

    fig, (ax_chute, ax_sol) = plt.subplots(1, 2, figsize=(14, 5.5), sharey=True)

    for nome, dados in resultados.items():
        cor = cores[nome]
        theta_tot = np.concatenate(([alpha], dados['solucao'], [beta]))
        chute_tot = np.concatenate(([alpha], dados['chute'], [beta]))

        ax_chute.plot(t_tot, chute_tot, color=cor, linewidth=2,
                      label=f"{nome}: {dados['texto']}")

        if nome == '24a':
            ax_sol.plot(t_tot, theta_tot, color=cor, linewidth=6, zorder=1,
                        label='24a (= 24b)')
        elif nome == '24b':
            ax_sol.plot(t_tot, theta_tot, color=cor, linewidth=2, linestyle='--',
                        zorder=2, label='24b')
        else:
            ax_sol.plot(t_tot, theta_tot, color=cor, linewidth=2.5, zorder=3,
                        label=nome)

    ax_chute.set_title('Chutes iniciais $\\theta_0(t)$')
    ax_sol.set_title('Soluções encontradas pelo Newton')

    for ax in (ax_chute, ax_sol):
        ax.set_xlabel('Tempo t')
        ax.grid(True, alpha=0.3)
        ax.axhline(alpha, color='gray', linewidth=0.8, linestyle=':')

    ax_chute.set_ylabel('Ângulo θ(t)')
    ax_chute.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fontsize='small')
    ax_sol.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize='small')

    fig.suptitle('Comparação de Diferentes Chutes Iniciais no Pêndulo Não Linear', fontsize=14)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()


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

    # --- Gráficos de comparação das soluções ---
    plotar_comparacao(t_tot, resultados, alpha, beta, 'graficos/comparacao_pendulo.png')
    plotar_comparacao_paineis(t_tot, resultados, alpha, beta, 'graficos/comparacao_pendulo_paineis.png')

# =============================================================================
# PARTE 2
# =============================================================================

def plotar_parte2(resultados, alpha, beta, nome, texto, filename):
    """Plotagem de todas as curvas em tempo absoluto, no mesmo gráfico."""
    plt.figure(figsize=(10, 6))

    cores = {20: '#E69F00', 50: '#0072B2', 100: '#CC79A7'}

    for T, (t_tot, theta_tot) in resultados.items():
        max_theta = np.max(theta_tot)
        cor_atual = cores.get(T, 'black')
        plt.plot(t_tot, theta_tot, color=cor_atual, label=f'T = {T} (max = {max_theta:.4f})', linewidth=2)

    plt.title(f'Chute: {texto} para T = 20,50 e 100')
    plt.xlabel('Tempo t')
    plt.ylabel('Ângulo θ(t)')
    plt.axhline(np.pi, color='black', linestyle='--', alpha=0.5, label=r'Assíntota $\theta = \pi$')
    plt.legend(loc='lower center')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

def exec_p2():
    alpha = 0.7
    beta = 0.7
    m = 500
    val_T = [20, 50, 100]

    chutes = {
        "constante_3": {
            "nome": "Constante 3",
            "func": lambda t, T: 3.0 * np.ones_like(t),
            "texto": r"$\theta_0(t) = 3$"
        }
    }

    for key, info in chutes.items():
        nome = info["nome"]
        texto = info["texto"]

        print(f"\n{'='*60}")
        print(f"Parte 2 com Chute: {nome}")
        print(f"{'='*60}")

        resultados = {}

        for T in val_T:
            h = T / (m + 1)
            t_i = np.linspace(h, T - h, m)
            t_tot = np.linspace(0, T, m + 2)

            chute = info["func"](t_i, T)
            theta_sol, hist_theta, hist_erro = pdl.newton(T, m, alpha, beta, chute)

            theta_tot = np.concatenate(([alpha], theta_sol, [beta]))
            print(f"-> Para T = {T:3}, o max(θ) é: {np.max(theta_sol):.6f}")

            resultados[T] = (t_tot, theta_tot)

        caminho = f'graficos/parte2_{key}.png'
        plotar_parte2(resultados, alpha, beta, nome, texto, caminho)

if __name__ == "__main__":
   #exec_p1()
    exec_p2()