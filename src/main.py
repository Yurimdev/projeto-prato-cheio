import sys
import os
import argparse
import json
from typing import List, Dict

# Garante que o diretório raiz está no path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import validate_quantity, format_donation_entry  # noqa: E402
from src.api import fetch_food_info  # noqa: E402

DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'donations.json')


def load_db() -> List[Dict]:
    """Carrega o banco de dados do arquivo JSON."""
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_db(db: List[Dict]):
    """Salva o banco de dados no arquivo JSON."""
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4)


def reset_db():
    """Limpa o arquivo de dados (usado pelos testes)."""
    save_db([])


def add_donation(donor: str, item: str, quantity: int) -> bool:
    """Adiciona uma nova doação ao sistema após validação e salva no arquivo."""
    if not donor.strip() or not item.strip():
        print("Erro: Nome do doador e item não podem ser vazios.")
        return False

    if not validate_quantity(quantity):
        print("Erro: A quantidade deve ser um número inteiro maior que zero.")
        return False

    db = load_db()
    entry = format_donation_entry(donor, item, quantity)
    db.append(entry)
    save_db(db)

    print(f"Sucesso: Doação de {quantity}x '{item}' por '{donor}' registrada!")
    return True


def list_donations() -> List[Dict]:
    """Retorna e imprime os itens doados a partir do arquivo."""
    db = load_db()

    if not db:
        print("Nenhuma doação registrada até o momento.")
        return []

    print("\n--- Lista de Doações ---")
    for idx, d in enumerate(db, 1):
        print(
            f"{idx}. Doador: {d['donor']} | "
            f"Item: {d['item']} | Qtd: {d['quantity']}"
        )
    print("------------------------\n")
    return db


def show_food_info(item: str) -> bool:
    """Busca e exibe dados do alimento via API Open Food Facts."""
    info = fetch_food_info(item)
    if info is None:
        print(f"Nao foi possivel obter dados externos para '{item}'.")
        return False

    print(f"\n--- Informacoes do Alimento: {item} ---")
    print(f"Produto:    {info['product_name']}")
    print(f"Marca:      {info['brands']}")
    print(f"Categorias: {info['categories']}")
    print(f"Nutri-Score: {info['nutriscore']}")
    print("------------------------------------------\n")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Projeto Prato Cheio - Sistema de Gestão de Doações"
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Comandos disponíveis"
    )

    # Comando de adicionar
    parser_add = subparsers.add_parser("add", help="Adicionar uma nova doação")
    parser_add.add_argument("--donor", required=True, help="Nome do doador")
    parser_add.add_argument("--item", required=True, help="Nome do item doado")
    parser_add.add_argument(
        "--qty", type=int, required=True, help="Quantidade doada"
    )

    # Comando de listar
    subparsers.add_parser("list", help="Listar doações registradas")

    # Comando de informações do alimento (consome API pública)
    parser_info = subparsers.add_parser(
        "info", help="Buscar dados do alimento na API Open Food Facts"
    )
    parser_info.add_argument(
        "--item", required=True, help="Nome do item para consultar na API"
    )

    args = parser.parse_args()

    if args.command == "add":
        add_donation(args.donor, args.item, args.qty)
    elif args.command == "list":
        list_donations()
    elif args.command == "info":
        show_food_info(args.item)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
