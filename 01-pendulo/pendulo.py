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

chute_inicial = 0.7 * np.ones(m)

# Chama a função principal
theta_solucao = newton(T, m, alpha, beta, chute_inicial)

print("\n--- Resultados ---")
print("Solução encontrada para os nós i:")
print(np.round(theta_solucao, 4))


### Plotagem 
t_tot = np.linspace(0, T, m + 2)
theta_tot = np.concatenate(([alpha], theta_solucao, [beta]))
chute_tot = np.concatenate(([alpha], chute_inicial, [beta]))


plt.figure(figsize=(8, 5))
plt.plot(t_tot, theta_tot, marker='o', color='blue', label='Solução Encontrada')
plt.plot(t_tot, chute_tot, linestyle='--', color='gray', label='Chute Inicial')

plt.title('Teste Provisório: Pêndulo Não Linear')
plt.xlabel('Tempo t')
plt.ylabel('Ângulo θ(t)')
plt.legend()
plt.grid(True)

plt.savefig('graficos/teste_pendulo3.png', dpi=300, bbox_inches='tight')
print("Gráfico salvo como 'teste_pendulo.png' na pasta atual!")