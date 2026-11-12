import importlib
import sys
from pathlib import Path

DIR_ATUAL = Path(__file__).resolve().parent
ROOT = DIR_ATUAL.parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import matplotlib
matplotlib.use("Agg")

ITEMS = {
    "a": ROOT / "resultados" / "item_a",
    "b": ROOT / "resultados" / "item_b",
    "c": ROOT / "resultados" / "item_c",
}


def garantir_pastas():
    for pasta in ITEMS.values():
        for subpasta in ("figuras", "dados", "tabelas"):
            (pasta / subpasta).mkdir(parents=True, exist_ok=True)

    # mantém compatibilidade com os diretórios já usados em outros experimentos
    (ROOT / "resultados" / "introducao" / "figuras").mkdir(parents=True, exist_ok=True)


def executar_experimento(nome_item, tp):
    modulo = importlib.import_module(f"exp_{nome_item}_{tp}")
    executar = getattr(modulo, "executar")
    executar()


def executar():
    print("=== Preparando estrutura de resultados ===")
    garantir_pastas()

    for nome in ("a", "b", "c"):
        print(f"\n=== Executando experimento {nome.upper()} Padrão")
        executar_experimento(nome, "padrao")

        print(f"\n=== Executando experimento {nome.upper()} Expandido")
        executar_experimento(nome, "expandido")

    print("\n=== Todos os experimentos foram executados com sucesso. ===")


if __name__ == "__main__":
    executar()
