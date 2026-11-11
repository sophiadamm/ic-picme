# Fluxo de tarefas: Exercício 5.22 (PVI de Motivação)

Stack: Python + NumPy + Matplotlib + pytest.

---

## Fase 0: Preparação

- [✓] Criar a estrutura de pastas:
- [✓] Criar `pyproject.toml` e `requirements.txt` (versões fixadas)
- [✓] Criar o ambiente virtual e rodar `pip install -e .`
- [✓] Organizar edição laTEX no VS Code
- [✓]  Introdução do Relatório


## Item A: Problema + Euler avançado + Euler recuado 
 
**Implementar**
- [✓] `problemas.py`
  - [✓] `dataclass PVI` (`f`, `dfdy`, `y0`, `exata` opcional, `nome`)
  - [✓] PVI motivação -> `motivacao()` e `g()`
- [ ] `metodos.py`
  - [✓] `euler_explicito` em `metodos.py` 
  - [✓] `euler_implicito` em `metodos.py` 
- [✓] `exp_a_padrao.py` e `exp_a_expandido.py` (`plotagem.py`) -> resultados (tabelas e gráficos) nos intervalos [0, 1.6] e [0, 5]
- [✓] `uteis.py`- ferramentas universais para os experimentos


**Relatório**
- [✓] Introdução/Objetivos do item a
- [✓] Implementação 
- [✓] Resultados e Discussão 
  - [✓] Análise experimento I (intervalo [0, 1.6])
  - [✓] Análise experimento II (intervalo [0, 5])
- [✓] Síntese/Conclusão Crítica (! Comparação dos Métodos)
---

## Item B:  Métodos Explícitos ( Euler e Runge-Kutta de Quarta Ordem)

**Implementar**
- [✓] `rf4` em `metodos.py`  
- [✓] `exp_b_rf4.py` e `plotagem.py` -> resultados (tabelas e graficos)


**Relatório**
- [] Introdução/Objetivos do item b
- [✓] Implementação 
- [] Resultados e Discussão 
  - [] Análise experimento I (intervalo [0, 1.6])
  - [] Análise experimento II (intervalo [0, 5])
- [] Síntese/Conclusão Crítica (! Comparação dos Métodos)


## Item C:  Métodos Implícitos ( Euler e Adams Moulton(2-step))
**Implementar**
- [] `adams_moulton` em `metodos.py`  
- [] `exp_c_adams_moulton.py` e `plotagem.py` -> resultados (tabelas e graficos)

**Relatório**
- [] Introdução/Objetivos do item b
- [] Implementação 
- [] Resultados e Discussão 
  - [] Análise experimento I (intervalo [0, 1.6])
  - [] Análise experimento II (intervalo [0, 5])
- [] Síntese/Conclusão Crítica (! Comparação dos Métodos)

## Item D:  Intervalos Mais Longos

## Extra: Soluções para os problemas encontrados

## Finalizar/Revisão Geral do Relatório

- [ ] Criar o `README.md` com um esqueleto de "como rodar"
- [ ] Conclusão do Relatório
- [ ] Revisão e Documentação dos códigos
- [ ] Estrutura do Relatório 
- [ ] Referências

[Introdução]
  - [] Completar descrição dos itens na primeira parte da introdução 
  - [?] Revisar a parte de ambiente computacional 
  - [?] Deixar tabela dos autovalores mais completa?

[Item A]
  - [] Resumir
  
[Item B]
  - []

[Item C]
  - []

[Item D]
  - []
