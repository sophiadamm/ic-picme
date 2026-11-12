import time
import numpy as np 
from scipy.optimize import newton

def euler_explicito(pvi, n, k):
    # Marca o início de execução para medição do tempo de CPU
    t0_cpu = time.perf_counter()
    
    # Pré-alocação dos vetores de tempo e solução numérica
    t_vals = np.zeros(n + 1)
    y_vals = np.zeros(n + 1)
    t_vals[0] = pvi.t0
    y_vals[0] = pvi.y0

    tn = pvi.t0
    Un = pvi.y0
    nfev = 0  # Contador de avaliações da função f
    
    # Contador de pontos válidos (para truncamento caso ocorra divergência)
    pts = 1 

    for i in range(n):
        # Cálculo exato do instante tn+1 para evitar acúmulo de erro numérico
        tn1 = pvi.t0 + (i + 1) * k   
        
        # Passo do Euler Explícito: U_{n+1} = U_n + k * f(t_n, U_n)
        Un1 = Un + k * pvi.f(tn, Un)
        nfev += 1  

        # Interrupção preventiva caso a solução exploda (NaN ou Inf)
        if not np.isfinite(Un1):
            print(f"Euler explícito explodiu em t = {tn1:.4f} (com passo k = {k})")
            break
        
        t_vals[i+1] = tn1
        y_vals[i+1] = Un1
        tn = tn1
        Un = Un1
        
        pts += 1

    # Marca o fim da execução do método    
    tf_cpu = time.perf_counter()

    # Empacotamento das estatísticas computacionais
    stats = {
        'nfev': nfev,
        'runtime': tf_cpu - t0_cpu,
    }
    
    return t_vals[:pts], y_vals[:pts], stats


def euler_implicito(pvi, n, k):
    # Marca o início de execução para medição do tempo de CPU
    t0_cpu = time.perf_counter()
    
    # Pré-alocação dos vetores de tempo e solução numérica
    t_vals = np.zeros(n + 1)
    y_vals = np.zeros(n + 1)
    t_vals[0] = pvi.t0
    y_vals[0] = pvi.y0

    tn = pvi.t0
    Un = pvi.y0
    nfev = 0  # Contador de avaliações de funções (f e dfdy)
    
    # Contador de pontos válidos (para truncamento caso ocorra divergência)
    pts = 1  

    for i in range(n):
        # Instante t_{n+1} calculado diretamente da malha
        tn1 = pvi.t0 + (i + 1) * k   

        # Resíduo da equação implícita: F(U) = U - U_n - k * f(t_{n+1}, U) = 0
        F  = lambda U: U - Un - k * pvi.f(tn1, U)
        # Derivada analítica dF/dU = 1 - k * df/dy(t_{n+1}, U) para o método de Newton
        dF = lambda U: 1 - k * pvi.dfdy(tn1, U)

        # Chute inicial via preditor de Euler Explícito: U^{(0)} = U_n + k * f(t_n, U_n)
        U0 = Un + k * pvi.f(tn, Un)
        nfev += 1  

        # Resolução da equação algébrica não linear via método de Newton
        Un1, info = newton(F, x0=U0, fprime=dF, tol=1e-12, maxiter=50,
                           full_output=True, disp=False)

        # Cada iteração do Newton avalia a função F e sua derivada dF
        nfev += info.iterations * 2

        # Interrupção se o método de Newton falhar em convergir ou gerar valor não finito
        if not info.converged or not np.isfinite(Un1):
            print(f"Euler implícito falhou em t = {tn1:.4f} (com passo k = {k})")
            break 

        t_vals[i+1] = tn1
        y_vals[i+1] = Un1
        Un = Un1
        tn = tn1
        
        pts += 1 

    # Marca o fim da execução do método
    tf_cpu = time.perf_counter()  
    
    # Empacotamento das estatísticas computacionais
    stats = {
        'nfev': nfev,
        'runtime': tf_cpu - t0_cpu,
    }

    return t_vals[:pts], y_vals[:pts], stats


def rk4(pvi, n, k):
    # Marca o início de execução para medição do tempo de CPU
    t0_cpu = time.perf_counter()
    
    # Pré-alocação dos vetores de tempo e solução numérica
    t_vals = np.zeros(n + 1)
    y_vals = np.zeros(n + 1)
    t_vals[0] = pvi.t0
    y_vals[0] = pvi.y0

    tn = pvi.t0
    Un = pvi.y0
    nfev = 0  # Contador de avaliações da função f
    
    # Contador de pontos válidos (para truncamento caso ocorra divergência)
    pts = 1 

    for i in range(n):
        # Estágio 1: inclinação no início do passo (tn)
        Y1 = Un
        F1 = pvi.f(tn, Y1)
        
        # Estágio 2: estimativa no ponto médio (tn + k/2) usando F1
        Y2 = Un + 0.5 * k * F1
        F2 = pvi.f(tn + 0.5 * k, Y2)
        
        # Estágio 3: nova estimativa no ponto médio (tn + k/2) usando F2
        Y3 = Un + 0.5 * k * F2
        F3 = pvi.f(tn + 0.5 * k, Y3)
        
        # Estágio 4: estimativa no final do passo (tn + k) usando F3
        Y4 = Un + k * F3
        F4 = pvi.f(tn + k, Y4)
        
        # Combinação ponderada (regra de Simpson) para obter U_{n+1}
        Un1 = Un + (k / 6.0) * (F1 + 2*F2 + 2*F3 + F4)
        tn1 = pvi.t0 + (i + 1) * k
        
        # O método RK4 clássico avalia a função f exatamente 4 vezes por passo
        nfev += 4  

        # Interrupção preventiva caso a solução exploda (NaN ou Inf)
        if not np.isfinite(Un1):
            print(f"RK4 explodiu em t = {tn1:.4f} (com passo k = {k})")
            break

        t_vals[i+1] = tn1
        y_vals[i+1] = Un1
        tn = tn1
        Un = Un1
        
        pts += 1
        
    # Marca o fim da execução do método
    tf_cpu = time.perf_counter()
    
    # Empacotamento das estatísticas computacionais
    stats = {
        'nfev': nfev,
        'runtime': tf_cpu - t0_cpu,
    }
    
    return t_vals[:pts], y_vals[:pts], stats


def adams_moulton(pvi, n, k):
    # Marca o início de execução para medição do tempo de CPU
    t0_cpu = time.perf_counter()
    
    # Pré-alocação dos vetores de tempo e solução numérica
    t_vals = np.zeros(n + 1)
    y_vals = np.zeros(n + 1)
    t_vals[0] = pvi.t0
    y_vals[0] = pvi.y0

    nfev = 0  # Contador de avaliações de funções (f e dfdy)
    pts = 1

    if n >= 1:
        # Inicialização do 1º passo (U_1 em t_1) via RK4 de 4ª ordem
        t_init, y_init, stats_init = rk4(pvi, 1, k)
        nfev += stats_init['nfev']

        if len(y_init) < 2 or not np.isfinite(y_init[1]):
            tf_cpu = time.perf_counter()
            return t_vals[:pts], y_vals[:pts], {'nfev': nfev, 'runtime': tf_cpu - t0_cpu}

        t_vals[1] = t_init[1]
        y_vals[1] = y_init[1]
        pts = 2

        # Armazena f_{i-1} = f(t_0, U_0) e f_i = f(t_1, U_1) para reutilização nos passos seguintes
        fn_1 = pvi.f(t_vals[0], y_vals[0])
        fn = pvi.f(t_vals[1], y_vals[1])
        nfev += 2

        Un = y_vals[1]

        # Laço principal do método Adams-Moulton de 2 passos (de i = 1 até n - 1)
        for i in range(1, n):
            tn1 = pvi.t0 + (i + 1) * k

            # Resíduo de Adams-Moulton (2-step): U - U_i - (k/12)*(-f_{i-1} + 8*f_i + 5*f(t_{i+1}, U)) = 0
            F  = lambda U: U - Un - (k / 12.0) * (-fn_1 + 8.0 * fn + 5.0 * pvi.f(tn1, U))
            # Derivada analítica dF/dU = 1 - (5k/12) * df/dy(t_{i+1}, U)
            dF = lambda U: 1.0 - (5.0 * k / 12.0) * pvi.dfdy(tn1, U)

            # Preditor explícito de Adams-Bashforth de 2 passos (AB2) como aproximação inicial
            U0 = Un + 0.5 * k * (3.0 * fn - fn_1)

            # Resolução da equação não linear implícita via método de Newton
            Un1, info = newton(F, x0=U0, fprime=dF, tol=1e-12, maxiter=50,
                               full_output=True, disp=False)

            # Cada iteração de Newton avalia F e dF
            nfev += info.iterations * 2

            # Interrupção caso Newton falhe em convergir ou gere valor não finito
            if not info.converged or not np.isfinite(Un1):
                print(f"Adams-Moulton (2-step) falhou em t = {tn1:.4f} (com passo k = {k})")
                break

            t_vals[i+1] = tn1
            y_vals[i+1] = Un1
            Un = Un1

            # Atualiza histórico de derivadas para o próximo passo
            fn_1 = fn
            fn = pvi.f(tn1, Un1)
            nfev += 1

            pts += 1

    # Marca o fim da execução do método
    tf_cpu = time.perf_counter()

    # Empacotamento das estatísticas computacionais
    stats = {
        'nfev': nfev,
        'runtime': tf_cpu - t0_cpu,
    }

    return t_vals[:pts], y_vals[:pts], stats