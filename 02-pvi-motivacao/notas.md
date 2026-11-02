# 1. Enunciado da Atividade (Exercise 5.22)

O **Exercise 5.22 (PVI Motivação: Métodos Explícitos e Implícitos)** requer a resolução numérica e análise do seguinte Problema de Valor Inicial (PVI):

$$y' = y^2 - g(x)$$
$$y(0) = 2$$

onde $g(x) = \frac{x^4 - 6x^3 + 12x^2 - 14x + 9}{(1+x)^2}$. A solução analítica exata é $y(x) = \frac{(1-x)(2-x)}{1+x}$. 

Com base neste PVI, as seguintes etapas devem ser desenvolvidas:

*   **(a)** Implementar os métodos de Euler Avançado (Explícito) e Euler Recuado (Implícito) e reproduzir os resultados mostrados na Figura 12.2 do material de referência no intervalo $[0, 1.6]$. É necessário escolher um método auxiliar para o cálculo de zero de função na formulação implícita.
*   **(b)** Implementar o método Explícito Runge-Kutta de Quarta Ordem (RK4) (conforme Exemplo 5.13, pág. 126 do livro de R. J. LeVeque) e resolver o PVI. Fornecer uma descrição crítica justificando as vantagens e desvantagens computacionais do RK4 em relação ao Euler Avançado, apoiada por argumentos teóricos e experimentos numéricos (gráficos e tabelas).
*   **(c)** Implementar o método Implícito Adams-Moulton de 2 passos (pág. 132 do livro de R. J. LeVeque) e resolver o PVI. Apresentar uma descrição crítica comparando suas vantagens e desvantagens computacionais em relação ao Euler Recuado, também utilizando teoria e experimentos numéricos.
*   **(d)** Elaborar uma síntese crítica sobre o emprego geral de métodos implícitos versus explícitos para PVIs. Avaliar e justificar o que ocorre ao tentar resolver este PVI nos intervalos $[0, 5]$, $[-2, 2]$ e $[-5, 40]$, incorporando argumentos e resultados dos itens anteriores.

---