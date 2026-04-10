import sys
import os
import argparse
import json
from typing import List, Dict

# Garante que o diretório raiz está no path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils import validate_quantity, format_donation_entry

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
        print(f"{idx}. Doador: {d['donor']} | Item: {d['item']} | Qtd: {d['quantity']}")
    print("------------------------\n")
    return db

def main():
    parser = argparse.ArgumentParser(description="Projeto Prato Cheio - Sistema de Gestão de Doações")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando de adicionar
    parser_add = subparsers.add_parser("add", help="Adicionar uma nova doação")
    parser_add.add_argument("--donor", required=True, help="Nome do doador")
    parser_add.add_argument("--item", required=True, help="Nome do item doado")
    parser_add.add_argument("--qty", type=int, required=True, help="Quantidade doada")

    # Comando de listar
    subparsers.add_parser("list", help="Listar doações registradas")

    args = parser.parse_args()

    if args.command == "add":
        add_donation(args.donor, args.item, args.qty)
    elif args.command == "list":
        list_donations()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
