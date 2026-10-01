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

### montar_G 
- Parametros: alpha, beta, passo(h), 