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

### Parâmetros iniciais 
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
    
    theta_sol, hist_theta, hist_erro = newton(T, m, alpha, beta, chute)
    resultados[nome] = {
        'solucao': theta_sol,
        'chute': chute,
        'texto': texto_func
    }
    
    exibir_relatorio(nome, texto_func, hist_erro)
    plotar_evolucao_newton(t_tot, hist_theta, alpha, beta, nome, texto_func, f'graficos/evolucao_{nome}.png')

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