# Fluxo de tarefas: Exercício 5.22 (PVI de Motivação)

Stack: Python + NumPy + Matplotlib + pytest.

---

## Fase 0: Preparação

- [✓] Criar a estrutura de pastas:
- [✓] Criar `pyproject.toml` e `requirements.txt` (versões fixadas)
- [✓] Criar o ambiente virtual e rodar `pip install -e .`
- [✓] Organizar edição laTEX no VS Code
- [ ] Criar o `README.md` com um esqueleto de "como rodar"


## Item A: Problema + Euler avançado + Euler recuado 
 
**Implementar**
- [✓] `problemas.py`
  - [✓] `dataclass PVI` (`f`, `dfdy`, `y0`, `exata` opcional, `nome`)
  - [✓] PVI motivação -> `motivacao()` e `g()`
- [ ] `metodos.py`
  - [✓] `euler_explicito` em `metodos.py` 
  - [✓] `euler_implicito` em `metodos.py` 
- [✓] `exp_a_fig122.py` e `plotagem.py` -> resultados (tabelas e graficos): h = 0.2, 0.1, 0.05 em [0, 1.6]
- [✓] `uteis.py`- ferramentas universais para os experimentos

**Relatório**
- [ ] Introdução/Objetivos do item a
- [ ] Implementação 
- [ ] Resultados e Discussão 
  - [ ] Entender (Comparação dos dois métodos e verificação da teoria)
  - [ ] Escrever

**Pronto quando:** testes da solução exata passam e a figura se parece com a Fig. 12.2.

---

## Item B:  Métodos Explícitos ( Euler e Runge-Kutta de Quarta Ordem)