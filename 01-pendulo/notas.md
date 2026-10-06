# Planejamento do Código: Resolução do PVC do Pêndulo Não Linear

## 1. Entradas e Parâmetros do Problema

Entrada -> 
 - Boundaries ( $\theta(0) = \alpha$ e $\theta(T) = \Beta$) -> Precido de $\alpha, \Beta, T$
 - Chute inicial do método de newton -> vetor de m elementos 

Saída -> 
- Pontos $\theta_i$
- Plotar gráfico (?)

Dependências -> 
- Numpy -> pra resolver o sistema linear (numpy.linalg.solve) - *verificar se não tem ferramenta melhor* - Usar Scipy?
- Matplotlib (?) 

## Procedimento Teórico de solução 

Objetivo - Encontrar raízes do sistema não linear $G(\theta) = \mathbf{0}$ utilizando o Método de Newton multivariável.

### 1. Discretização do domínio 
- $t \in [0, T]$ é dividido em $m+1$ subintervalos.O intervalo contínuo de tempo 
- Passo: $h = \frac{T}{m+1}$.
- Vetor de tempo: $t_i = i \cdot h$, para $i = 0, 1, \dots, m+1$.
- Condições de contorno: $\theta_0 = \alpha$ e $\theta_{m+1} = \beta$.
- Incógnitas: O vetor $\theta$  contendo os pontos internos $[\theta_1, \theta_2, \dots, \theta_m]^T$. 
- Montar o gráfico vai ser usar o vetor de $t$ e de $\theta$

### 2. Função G 
$$G_i(\theta) = \frac{\theta_{i-1} - 2\theta_i + \theta_{i+1}}{h^2} + \sin(\theta_i)$$

Para $i = 1$: o termo $\theta_{i-1}$ é substituído pela condição inicial $\alpha$.

Para $i = m$: o termo $\theta_{i+1}$ é substituído pela condição final $\beta$.

### 3. Matriz Jacobiana 
- Diagonal Principal ($i = j$): $\frac{\partial G_i}{\partial \theta_i} = -\frac{2}{h^2} + \cos(\theta_i)$
- Diagonais Secundárias ($i = j \pm 1$): $\frac{\partial G_i}{\partial \theta_{i \pm 1}} = \frac{1}{h^2}$
- Todos os outros elementos são zero.

### 4. Iterações 
1. Avaliar $G(\theta^{[k]})$ e $J(\theta^{[k]})$.
2. Resolver o sistema linear para encontrar o passo de atualização $\delta^{[k]}$:$$J(\theta^{[k]}) \cdot \delta^{[k]} = -G(\theta^{[k]})$$
3. Atualizar a solução:$$\theta^{[k+1]} = \theta^{[k]} + \delta^{[k]}$$

### 5. Critério de Parada
- Que norma eu uso? 
- Que tolerância?
- Que limite máximo 
- Preciso fazer alguma implementação especial quando diverge? 

## 3. Prática 

1. Arquivo de módulo -> apenas recebe dados, faz as contas e devolve a resposta.
    - funções: montar_G, montar_J, newton
    - Entradas da função principal: T, m, theta_0 (condição inicial), theta_final e o chute_inicial.
    - Saída: Apenas o vetor $\theta$ resolvido (ou até mesmo uma tupla retornando o vetor e o número de iterações que levou para convergir).

2. Main - > desenvolver ainda 

### Resultados 
--- Resumo: 24a | $\theta_0(t) = 0.7\cos(t) + 0.5\sin(t)$ ---
Iteração   | Erro (Norma Infinito)    
-------------------------------------------------------
1          | 3.2932e-01               
2          | 1.7490e-01               
3          | 3.0646e-02               
4          | 2.2845e-04               
5          | 1.4027e-08               
6          | 8.0423e-15               
-> Convergiu em 6 iterações.


--- Resumo: 24b | $\theta_0(t) = 0.7$ ---
Iteração   | Erro (Norma Infinito)    
-------------------------------------------------------
1          | 1.7545e+00               
2          | 3.9297e-01               
3          | 5.7972e-02               
4          | 6.0345e-04               
5          | 2.6636e-08               
6          | 4.6732e-14               
7          | 3.0694e-14               
8          | 3.7275e-14               
9          | 7.9529e-14               
10         | 2.9656e-14               
11         | 2.2536e-14               
12         | 2.4181e-14               
13         | 4.7379e-14               
14         | 6.2591e-14               
15         | 6.6519e-14               
16         | 4.3483e-14               
17         | 3.9266e-14               
18         | 1.1496e-14               
19         | 1.4485e-14               
20         | 2.6920e-14               
21         | 7.7391e-14               
22         | 5.9343e-14               
23         | 2.8996e-14               
24         | 6.8630e-14               
25         | 1.2479e-14               
26         | 1.8898e-14               
27         | 5.0995e-15               
-> Convergiu em 27 iterações.


--- Resumo: 25 | $\theta_0(t) = 0.7 + \sin(t/2)$ ---
Iteração   | Erro (Norma Infinito)    
-------------------------------------------------------
1          | 4.2044e+00               
2          | 5.3935e+00               
3          | 8.2274e+00               
4          | 7.5052e-01               
5          | 4.0620e-02               
6          | 2.5721e-04               
7          | 1.2040e-08               
8          | 7.9701e-15               
-> Convergiu em 8 iterações.


--- Resumo: Customizado | $\theta_0(t) = 0.7 + \sin(4t)$ ---
Iteração   | Erro (Norma Infinito)    
-------------------------------------------------------
1          | 3.8000e+00               
2          | 1.3663e+00               
3          | 4.7993e-01               
4          | 8.0304e-02               
5          | 2.7642e-03               
6          | 3.3397e-06               
7          | 4.8611e-12               
8          | 2.1832e-14               
9          | 2.6217e-14               
10         | 3.7046e-14               
11         | 4.1206e-14               
12         | 3.3409e-14               
13         | 2.4153e-14               
14         | 9.2400e-15               
-> Convergiu em 14 iterações.

