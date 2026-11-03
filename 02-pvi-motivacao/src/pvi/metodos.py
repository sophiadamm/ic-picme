import time
import numpy as np 
from scipy.optimize import newton

def euler_explicito(pvi, n, k):
    t0_cpu = time.perf_counter()
    
    t_vals = np.zeros(n + 1)
    y_vals = np.zeros(n + 1)
    t_vals[0] = pvi.t0
    y_vals[0] = pvi.y0

    tn = pvi.t0
    Un = pvi.y0
    nfev = 0  
    
    # Contador para saber exatamente onde cortar os arrays no final
    pts = 1 

    for i in range(n):
        tn1 = pvi.t0 + (i + 1) * k   
        Un1 = Un + k * pvi.f(tn, Un)
        nfev += 1  

        if not np.isfinite(Un1):
            print(f"Euler explícito explodiu em t = {tn1:.4f} (com passo k = {k})")
            break
        
        t_vals[i+1] = tn1
        y_vals[i+1] = Un1
        tn = tn1
        Un = Un1
        
        pts += 1
        
    tf_cpu = time.perf_counter()
    
    stats = {
        'nfev': nfev,
        'runtime': tf_cpu - t0_cpu,
    }
    
    return t_vals[:pts], y_vals[:pts], stats


def euler_implicito(pvi, n, k):
    t0_cpu = time.perf_counter()
    
    t_vals = np.zeros(n + 1)
    y_vals = np.zeros(n + 1)
    t_vals[0] = pvi.t0
    y_vals[0] = pvi.y0

    tn = pvi.t0
    Un = pvi.y0
    
    nfev = 0  
    
    pts = 1  

    for i in range(n):
        tn1 = pvi.t0 + (i + 1) * k   

        F  = lambda U: U - Un - k * pvi.f(tn1, U)
        dF = lambda U: 1 - k * pvi.dfdy(tn1, U)

        U0 = Un + k * pvi.f(tn, Un)
        nfev += 1  

        Un1, info = newton(F, x0=U0, fprime=dF, tol=1e-12, maxiter=50,
                           full_output=True, disp=False)

        nfev += info.iterations * 2

        if not info.converged or not np.isfinite(Un1):
            print(f"Euler implícito falhou em t = {tn1:.4f} (com passo k = {k})")
            break 

        t_vals[i+1] = tn1
        y_vals[i+1] = Un1
        Un = Un1
        tn = tn1
        
        pts += 1 

    tf_cpu = time.perf_counter()  
    
    stats = {
        'nfev': nfev,
        'runtime': tf_cpu - t0_cpu,
    }

    return t_vals[:pts], y_vals[:pts], stats