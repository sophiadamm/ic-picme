import numpy as np
import matplotlib.pyplot as plt


def montar_G(theta, h, alpha, beta):
    """Constrói o vetor de resíduos G(theta) para as diferenças finitas."""
    m = len(theta)
    G = np.zeros(m) 

    # Itera sobre todos os pontos internos da malha
    for i in range(m): 
        # Aplica a condição de contorno inicial (alpha) no primeiro ponto
        if i == 0: 
            theta_prev = alpha 
        else: 
            theta_prev = theta[i-1]

        # Aplica a condição de contorno final (beta) no último ponto
        if i == m-1: 
            theta_pos = beta
        else: 
            theta_pos = theta[i+1]

        # Equação de diferenças centradas + termo não linear do pêndulo
        G[i] = 1/(h*h)*(theta_prev - 2*theta[i] + theta_pos) + np.sin(theta[i])
    
    return G

def montar_J(theta, h):
    """Monta a matriz Jacobiana tridiagonal J(theta)."""
    m = len(theta)

    # Define os elementos das diagonais
    dp = -2 + h**2 * np.cos(theta) # Diagonal principal
    vs = np.ones(m-1)              # Diagonais superior e inferior

    # Constrói as matrizes diagonais e soma
    main = np.diag(dp, k=0)
    sup = np.diag(vs, k=1)
    inf = np.diag(vs, k=-1)
        
    J = 1/(h**2) * (main + sup + inf)
    
    return J

def newton(T, m, alpha, beta, chute_inicial, tol=1e-14, max_iter=50):
    """Executa o Método de Newton multivariável para encontrar a raiz de G(theta) = 0."""
    h = T / (m + 1)
    
    theta = np.copy(chute_inicial)

    # Armazena o histórico para análise de convergência e plotagem
    hist_theta = [np.copy(theta)]
    hist_erro = []

    for k in range(max_iter):
        G = montar_G(theta, h, alpha, beta)
        J = montar_J(theta, h)

        # Resolve o sistema linear J * v = -G para encontrar o passo de atualização (v)
        try:
            v = np.linalg.solve(J, -G)
        except np.linalg.LinAlgError:
            print(f"Erro na iteração {k}: A matriz Jacobiana não pôde ser invertida.")
            hist_erro.append(float('inf'))
            break

        # Atualiza a solução
        theta = theta + v

        # Calcula o erro usando a norma do infinito
        erro = np.linalg.norm(v, ord=np.inf)

        hist_theta.append(np.copy(theta))
        hist_erro.append(erro)

        # Critério de parada
        if erro < tol:
            break
    
    return theta, hist_theta, hist_erro

def exibir_relatorio(nome_teste, texto_funcao, hist_erro):
    """Imprime uma tabela no terminal com a evolução do erro a cada iteração."""
    print(f"\n--- Resumo: {nome_teste} | {texto_funcao} ---")
    print(f"{'Iteração':<10} | {'Erro (Norma Infinito)':<25}")
    print("-" * 55)
    for k, erro in enumerate(hist_erro):
        print(f"{k+1:<10} | {erro:<25.4e}")

    # Verifica se a convergência atingiu um nível aceitável
    if hist_erro and hist_erro[-1] < 1e-14:
        print(f"-> Convergiu em {len(hist_erro)} iterações.\n")
    else:
        print(f"-> NÃO convergiu ou erro numérico.\n")

def plotar_evolucao_newton(t_tot, historico_theta, alpha, beta, nome_teste, texto_funcao, filename):
    """Gera um gráfico mostrando a evolução do vetor theta desde o chute inicial até a solução final."""
    plt.figure(figsize=(10, 6))
    num_iteracoes = len(historico_theta)

    # Cria um gradiente de cores para ilustrar o avanço das iterações
    cores = plt.cm.viridis(np.linspace(0.3, 1, num_iteracoes))
    
    for i, curr_t in enumerate(historico_theta):
        # Reconecta as condições de contorno (alpha e beta) para a plotagem
        theta_tot = np.concatenate(([alpha], curr_t, [beta]))
        
        # Destaca a última iteração (solução final) com uma linha mais grossa
        linewidth = 2.5 if i == num_iteracoes - 1 else 1.0
        # Deixa o chute inicial pontilhado
        linestyle = '--' if i == 0 else '-'
        
        plt.plot(t_tot, theta_tot, color=cores[i], linewidth=linewidth, linestyle=linestyle)

    #Montagem do gráfico que será salvo em png
    plt.title(f'Evolução do Método de Newton - {nome_teste}\nChute: {texto_funcao}')
    plt.xlabel('Tempo t')
    plt.ylabel('Ângulo θ(t)')
    plt.legend(loc='best', fontsize='small')
    plt.grid(True, alpha=0.3)
    
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()