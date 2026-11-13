# Iniciação Científica — PICME

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

Repositório de implementações numéricas, experimentos computacionais e relatórios desenvolvidos durante o programa de **Iniciação Científica (PICME / OBMEP - CNPq)** na Universidade Estadual de Campinas (**UNICAMP**)

---

## 📌 Sumário

- [Visão Geral](#-visão-geral)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Módulos e Atividades](#-módulos-e-atividades)
  - [01. PVC do Pêndulo Não Linear](#1-pvc-do-pêndulo-não-linear-01-pendulo)
  - [02. Análise de PVIs e Estabilidade Numérica](#2-análise-de-pvis-e-estabilidade-numérica-02-pvi-motivacao)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Executar os Experimentos](#-como-executar-os-experimentos)
  - [Experimentos do Pêndulo](#experimentos-do-pêndulo)
  - [Experimentos de PVIs](#experimentos-de-pvis)
  - [Compilação do Relatório em LaTeX](#compilação-do-relatório-em-latex)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Referências Bibliográficas](#-referências-bibliográficas)
- [Autoria e Créditos](#-autoria-e-créditos)

---

## 📖 Visão Geral

Este repositório reúne estudos teóricos e experimentais em análise numérica aplicados a equações diferenciais ordinárias (EDOs):
1. **Problemas de Valor de Contorno (PVCs):** Discretização via Diferenças Finitas e resolução de sistemas não lineares pelo Método de Newton multivariável.
2. **Problemas de Valor Inicial (PVIs):** Investigação de métodos numéricos de passo único e de passos múltiplos, comparando abordagens explícitas e implícitas quanto à ordem de convergência, estabilidade absoluta, custo computacional e comportamento diante de problemas rígidos (*stiff*) e singularidades.

---

## 📂 Estrutura do Repositório

```text
ic-picme/
├── 01-pendulo/                   # Atividade 1: PVC do Pêndulo Não Linear
│   ├── graficos/                 # Gráficos gerados (comparações, evoluções de Newton)
│   ├── main.py                   # Script de execução dos experimentos (Partes 1 e 2)
│   ├── pendulo.py                # Implementação das funções G, Jacobiana e Newton
│   └── notas.md                  # Deduções teóricas e anotações de planejamento
├── 02-pvi-motivacao/             # Atividade 2: Métodos Explícitos e Implícitos para PVIs
│   ├── Enunciado-Atividade2.pdf   # Guia e especificações da atividade
│   ├── experimentos/             # Scripts executáveis de cada etapa/experimento
│   │   ├── exp_intro_*.py        # Dinâmica analítica, autovalores e estabilidade
│   │   ├── exp_a_*.py            # Item (a): Euler Explícito vs. Euler Recuado
│   │   ├── exp_b_*.py            # Item (b): RK4 vs. Euler Explícito
│   │   ├── exp_c_*.py            # Item (c): Adams-Moulton (2 passos) vs. Euler Recuado
│   │   ├── exp_d_*.py            # Item (d): Singularidades (t = -1) e domínios longos
│   │   └── exp_global.py         # Bateria consolidada de testes
│   ├── relatorio/                # Relatório acadêmico detalhado em LaTeX
│   │   ├── main.tex              # Código-fonte principal do documento
│   │   └── main.pdf              # Documento compilado
│   ├── resultados/               # Figuras, tabelas e dados exportados pelos experimentos
│   └── src/pvi/                  # Pacote Python reutilizável com os solvers e rotinas
│       ├── __init__.py
│       ├── metodos.py            # Euler Explícito, Euler Implícito, RK4, Adams-Moulton
│       ├── problemas.py          # Definição formal da classe PVI e do problema teste
│       ├── plotagem.py           # Rotinas de visualização e gráficos comparativos
│       └── uteis.py              # Análise de erros, ordens, autovalores e métricas
├── pyproject.toml                # Configuração do pacote Python para instalação editável
├── requirements.txt              # Dependências do projeto fixadas
└── README.md                     # Documentação geral do repositório
```

---

## 🔬 Módulos e Atividades

### 1. PVC do Pêndulo Não Linear (`01-pendulo/`)

Aborda a resolução do problema de valor de contorno com condições de Dirichlet:
$$\begin{cases}
\theta''(t) + \sin(\theta(t)) = 0, \quad t \in [0, T] \\
\theta(0) = \alpha, \quad \theta(T) = \beta
\end{cases}$$

- **Discretização:** Malha uniforme com passo $h = \frac{T}{m+1}$ aproximada por diferenças finitas centrais de segunda ordem:
  $$\frac{\theta_{i-1} - 2\theta_i + \theta_{i+1}}{h^2} + \sin(\theta_i) = 0$$
- **Solução Numérica:** Montagem do sistema algébrico não linear $G(\theta) = \mathbf{0}$ e resolução por **Método de Newton multivariável**:
  $$J(\theta^{[k]}) \, \delta^{[k]} = -G(\theta^{[k]}), \quad \theta^{[k+1]} = \theta^{[k]} + \delta^{[k]}$$
  em que a Jacobiana $J$ possui estrutura tridiagonal esparsa.
- **Análises:**
  - Sensibilidade ao chute inicial $\theta_0(t)$ (bacias de atração e convergência para diferentes modos de oscilação).
  - Comportamento assintótico e múltiplos equilíbrios em intervalos temporais longos ($T = 20, 50, 100$).

---

### 2. Análise de PVIs e Estabilidade Numérica (`02-pvi-motivacao/`)

Estudo aprofundado baseado no problema de motivação (Süli & Mayers, Cap. 12; LeVeque, Cap. 5):
$$\begin{cases}
y'(t) = y(t)^2 - g(t), \quad t \in [t_0, T] \\
y(t_0) = y_0
\end{cases}$$
com termo fonte $g(t)$ construído de modo que a solução exata seja:
$$y(t) = \frac{(1 - t)(2 - t)}{1 + t}, \quad \text{possuindo singularidade em } t = -1$$

O autovalor local da linearização é dado por $\lambda(t) = \frac{\partial f}{\partial y}(t, y(t)) = 2y(t)$, induzindo regimes de rigidez transitória e instabilidade dependendo do sinal e magnitude de $y(t)$.

#### Métodos Implementados (`src/pvi/metodos.py`)
| Método | Tipo | Ordem | Resolução do Passo |
| :--- | :--- | :---: | :--- |
| **Euler Explícito (Progressivo)** | Passo único, Explícito | $\mathcal{O}(k)$ | $U_{n+1} = U_n + k f(t_n, U_n)$ |
| **Euler Implícito (Recuado)** | Passo único, Implícito | $\mathcal{O}(k)$ | Equação não linear resolvida via Newton escalar |
| **Runge-Kutta 4 (RK4)** | Estágios múltiplos, Explícito | $\mathcal{O}(k^4)$ | Combinação linear de 4 avaliações de $f$ |
| **Adams-Moulton (2 passos)** | Passos múltiplos, Implícito | $\mathcal{O}(k^3)$ / $\mathcal{O}(k^4)$ | Implícito resolvido iterativamente com inicialização adequada |

#### Roteiro dos Experimentos
- **Item (a):** Reprodução da Figura 12.2 de Süli & Mayers no intervalo $[0, 1.6]$, ilustrando a instabilidade explosiva do Euler Explícito para passos acima do limite crítico de estabilidade ($k > k_{\text{crit}}$) e o amortecimento estável do Euler Implícito.
- **Item (b):** Comparação entre RK4 e Euler Explícito: ganho de precisão de quarta ordem, ampliação da região de estabilidade e análise de custo por passo versus precisão global.
- **Item (c):** Comparação entre Adams-Moulton e Euler Implícito: ganho em ordem de convergência, custo das iterações de ponto fixo/Newton e conservação de estabilidade.
- **Item (d):** Testes em intervalos não convencionais:
  - Domínios atravessando a singularidade polar em $t = -1$ (ex.: $[-2, 2]$ e $[-5, 40]$), com salvaguardas de detecção de polos e interrupção controlada.
  - Dinâmica para tempos longos $[0, 40]$, mostrando estabilidade assintótica e custo acumulado ($N_{\text{fev}}$ e tempo de CPU).

---

## 🚀 Instalação e Configuração

### Pré-requisitos
- **Python 3.10** ou superior
- **Ambiente virtual** (`venv` ou `conda`)
- *(Opcional, para compilar o relatório)* Distribuição TeX Live com suporte a `minted` e Pygments.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/sophiazogaib/ic-picme.git
   cd ic-picme
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Instale o pacote `pvi` em modo desenvolvimento:**
   ```bash
   pip install -e .
   ```
   *Isso disponibiliza o módulo `pvi` para importação direta em qualquer script Python do projeto.*

---

## 💻 Como Executar os Experimentos

### Experimentos do Pêndulo
Para executar os experimentos do PVC e gerar as curvas de convergência em `01-pendulo/graficos/`:
```bash
cd 01-pendulo
python main.py
cd ..
```

### Experimentos de PVIs
Os experimentos estão estruturados dentro de `02-pvi-motivacao/experimentos/`. Podem ser executados individualmente:

```bash
# Análise de autovalores e estabilidade teórica
python 02-pvi-motivacao/experimentos/exp_intro_autovalores.py
python 02-pvi-motivacao/experimentos/exp_intro_estabilidade.py

# Item (a): Euler Explícito vs. Implícito no intervalo padrão
python 02-pvi-motivacao/experimentos/exp_a_padrao.py

# Item (b): Avaliação de RK4 e passos críticos
python 02-pvi-motivacao/experimentos/exp_b_padrao.py

# Item (c): Método de Adams-Moulton
python 02-pvi-motivacao/experimentos/exp_c_padrao.py

# Item (d): Singularidades e horizontes longos de integração
python 02-pvi-motivacao/experimentos/exp_d_singularidade.py
python 02-pvi-motivacao/experimentos/exp_d_Tlongo.py

# Bateria completa e busca crítica automatizada
python 02-pvi-motivacao/experimentos/exp_global.py
```
Os gráficos e tabelas resultantes serão salvos automaticamente nos respectivos subdiretórios em `02-pvi-motivacao/resultados/`.

### Compilação do Relatório em LaTeX
O relatório completo da Atividade 2 encontra-se em `02-pvi-motivacao/relatorio/main.tex`. Para compilá-lo (necessita da flag `-shell-escape` para o pacote `minted`):

```bash
cd 02-pvi-motivacao/relatorio
latexmk -pdf -shell-escape main.tex
# ou diretamente:
pdflatex -shell-escape main.tex
cd ../..
```

---

## 🛠 Tecnologias Utilizadas

- **Linguagem Principal:** Python 3.10+
- **Computação Científica:**
  - [NumPy](https://numpy.org/) — manipulação vetorial, matrizes esparsas e álgebra linear.
  - [SciPy](https://scipy.org/) — métodos de busca de raízes (`scipy.optimize.newton`).
- **Visualização de Dados:**
  - [Matplotlib](https://matplotlib.org/) — geração de gráficos vetoriais e mapas de estabilidade com qualidade para publicação.
- **Tipografia Científica:**
  - LaTeX / TikZ / Minted — diagramação técnica e equacionamento formal.

---

## 📚 Referências Bibliográficas

1. **SÜLI, Endre; MAYERS, David F.** *An Introduction to Numerical Analysis*. Cambridge University Press, 2003. (Capítulo 12: *Initial Value Problems for Ordinary Differential Equations*).
2. **LEVEQUE, Randall J.** *Finite Difference Methods for Ordinary and Partial Differential Equations: Steady-State and Time-Dependent Problems*. SIAM, 2007.
3. **HAIRER, Ernst; WANNER, Gerhard.** *Solving Ordinary Differential Equations II: Stiff and Differential-Algebraic Problems*. Springer-Verlag, 1996.
4. **BURDEN, Richard L.; FAIRES, J. Douglas.** *Numerical Analysis*. 9ª ed., Cengage Learning, 2010.

---

## 👩‍💻 Autoria e Créditos

Desenvolvido por **Sophia Damm Zogaib Mardones** como parte das atividades de Iniciação Científica do **PICME** na **Universidade Estadual de Campinas (UNICAMP)**.

*Para fins acadêmicos e educacionais.*
