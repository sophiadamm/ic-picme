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

    for k in range(max_iter):
        G = montar_G(theta, h, alpha, beta)
        J = montar_J(theta, h)

        try:
            v = np.linalg.solve(J, -G)
        except np.linalg.LinAlgError:
            print(f"Erro na iteração {k}: A matriz Jacobiana é singular ou não pôde ser invertida.")
            break
        theta = theta + v

        erro = np.linalg.norm(v, ord=np.inf)

        print(f"{k} | {erro}")

        if erro < tol:
            print(f"Convergência na iteração {k+1}!")
            return theta
    
    print(f"O método não convergiu após {max_iter} iterações. Erro atual é {erro}")
    return theta

### Testes provisórios 
alpha = 0.7
beta = 0.7
T = 2 * math.pi
m = 500
h = T / (m + 1)
t_i = np.linspace(h, T - h, m)

theta_0_24a = 0.7*np.cos(t_i) + 0.5*np.sin(t_i) 
theta_0_24b = 0.7 * np.ones(m)
theta_0_25 = 0.7 + np.sin(t_i/2)
theta_0 = 0.7 + np.sin(t_i*4)

theta_sol_24a = newton(T, m, alpha, beta, theta_0_24a)
theta_sol_24b = newton(T, m, alpha, beta, theta_0_24b)
theta_sol_25  = newton(T, m, alpha, beta, theta_0_25)
theta_sol = newton(T, m, alpha, beta, theta_0) 

t_tot = np.linspace(0, T, m + 2)

theta_tot_24a = np.concatenate(([alpha], theta_sol_24a, [beta]))
theta_tot_24b = np.concatenate(([alpha], theta_sol_24b, [beta]))
theta_tot_25  = np.concatenate(([alpha], theta_sol_25, [beta]))
theta_tot= np.concatenate(([alpha], theta_sol, [beta]))

chute_tot_24a = np.concatenate(([alpha], theta_0_24a, [beta]))
chute_tot_24b = np.concatenate(([alpha], theta_0_24b, [beta]))
chute_tot_25  = np.concatenate(([alpha], theta_0_25, [beta]))
chute_tot = np.concatenate(([alpha], theta_0, [beta]))

plt.figure(figsize=(10, 6))

plt.plot(t_tot, theta_tot_24a, marker='o', color='blue', label='Solução 24a')
plt.plot(t_tot, theta_tot_24b, marker='s', color='green', label='Solução 24b')
plt.plot(t_tot, theta_tot_25, marker='^', color='red', label='Solução 25')
plt.plot(t_tot, theta_tot, marker='*', color='purple', markersize=8, label='Solução Customizada')

plt.plot(t_tot, chute_tot_24a, linestyle='--', color='blue', alpha=0.4, label='Chute 24a')
plt.plot(t_tot, chute_tot_24b, linestyle='--', color='green', alpha=0.4, label='Chute 24b')
plt.plot(t_tot, chute_tot_25, linestyle='--', color='red', alpha=0.4, label='Chute 25')
plt.plot(t_tot, chute_tot, linestyle='--', color='purple', alpha=0.5, label='Chute Customizado')

plt.title('Comparação de Diferentes Chutes Iniciais no Pêndulo Não Linear')
plt.xlabel('Tempo t')
plt.ylabel('Ângulo θ(t)')
plt.legend(loc='best', fontsize='small') 
plt.grid(True)

plt.savefig('graficos/comparacao_pendulo1.png', dpi=300, bbox_inches='tight')
print("Gráfico salvo como 'comparacao_pendulo.png' na pasta graficos!")