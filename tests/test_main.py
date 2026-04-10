import pytest
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import add_donation, list_donations, reset_db
from src.utils import validate_quantity

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    # Setup: limpa o DB antes de cada teste
    reset_db()
    yield
    # Teardown: limpa o DB depois de cada teste
    reset_db()

# Teste 1: Caminho Feliz (Sucesso)
def test_add_donation_success(capsys):
    """Valida se uma doação válida é adicionada corretamente."""
    result = add_donation("Maria", "Arroz", 5)
    assert result is True
    
    donations = list_donations()
    assert len(donations) == 1
    assert donations[0] == {"donor": "Maria", "item": "Arroz", "quantity": 5}

# Teste 2: Entrada Inválida (Quantidade negativa)
def test_add_donation_negative_quantity(capsys):
    """Impede valor negativo na adição de doações."""
    result = add_donation("João", "Feijão", -2)
    assert result is False
    
    donations = list_donations()
    assert len(donations) == 0

# Teste 3: Caso Limite (Quantidade zero)
def test_validate_quantity_zero():
    """Valida caso limite onde a quantidade é zero (não deve ser permitida)."""
    assert validate_quantity(0) is False
