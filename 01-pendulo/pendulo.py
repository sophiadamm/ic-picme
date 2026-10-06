import numpy as np
import matplotlib.pyplot as plt
import math


def montar_G(theta, h, alpha, beta):
    m = len(theta)
    G = np.zeros(m) 
    
    for i in range(m): 
        if i == 0: 
            theta_prev = alpha 
        else: 
            theta_prev = theta[i-1]

        if i == m-1: 
            theta_pos = beta
        else: 
            theta_pos = theta[i+1]

        G[i] = 1/(h*h)*(theta_prev - 2*theta[i] + theta_pos) + np.sin(theta[i])
    
    return G

def montar_J(theta, h):
    m = len(theta)

    dp = -2 + h**2*np.cos(theta)
    vs = np.ones(m-1)

    main = np.diag(dp, k=0)
    sup = np.diag(vs, k=1)
    inf = np.diag(vs, k=-1)
    J = 1/(h**2)*(main + sup + inf)
    
    return J

def newton(T, m, alpha, beta, chute_inicial, tol=1e-14, max_iter=100):
    h = T / (m + 1)
    
    theta = np.copy(chute_inicial)

    hist_theta = [np.copy(theta)]
    hist_erro = []

    for k in range(max_iter):
        G = montar_G(theta, h, alpha, beta)
        J = montar_J(theta, h)

        try:
            v = np.linalg.solve(J, -G)
        except np.linalg.LinAlgError:
            print(f"Erro na iteração {k}: A matriz Jacobiana é singular ou não pôde ser invertida.")
            hist_erro.append(float('inf'))
            break
        theta = theta + v

        erro = np.linalg.norm(v, ord=np.inf)

        hist_theta.append(np.copy(theta))
        hist_erro.append(erro)

        if erro < tol:
            break
    
    return theta, hist_theta, hist_erro

def exibir_relatorio(nome_teste, texto_funcao, hist_erro):
    print(f"\n--- Resumo: {nome_teste} | {texto_funcao} ---")
    print(f"{'Iteração':<10} | {'Erro (Norma Infinito)':<25}")
    print("-" * 55)
    for k, erro in enumerate(hist_erro):
        print(f"{k+1:<10} | {erro:<25.4e}")
    
    if hist_erro and hist_erro[-1] < 1e-14:
        print(f"-> Convergiu em {len(hist_erro)} iterações.\n")
    else:
        print(f"-> NÃO convergiu ou erro numérico.\n")

def plotar_evolucao_newton(t_tot, historico_theta, alpha, beta, nome_teste, texto_funcao, filename):
    plt.figure(figsize=(10, 6))
    num_iteracoes = len(historico_theta)
    cores = plt.cm.viridis(np.linspace(0.3, 1, num_iteracoes))
    
    for i, curr_t in enumerate(historico_theta):
        theta_tot = np.concatenate(([alpha], curr_t, [beta]))
        linewidth = 2.5 if i == num_iteracoes - 1 else 1.0
        linestyle = '--' if i == 0 else '-'
        
        plt.plot(t_tot, theta_tot, color=cores[i], linewidth=linewidth, linestyle=linestyle)

    plt.title(f'Evolução do Método de Newton - {nome_teste}\nChute: {texto_funcao}')
    plt.xlabel('Tempo t')
    plt.ylabel('Ângulo θ(t)')
    plt.legend(loc='best', fontsize='small')
    plt.grid(True, alpha=0.3)
    
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()