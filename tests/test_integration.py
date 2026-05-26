import sys
import os
from unittest.mock import patch, MagicMock

import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api import fetch_food_info  # noqa: E402


FAKE_RESPONSE = {
    "products": [
        {
            "product_name": "Arroz Branco",
            "brands": "Marca Teste",
            "categories": "Cereais, Arroz",
            "nutriscore_grade": "a",
        }
    ]
}


@patch("src.api.requests.get")
def test_fetch_food_info_success(mock_get):
    """Valida o parsing da resposta da API Open Food Facts (fluxo feliz)."""
    mock_response = MagicMock()
    mock_response.json.return_value = FAKE_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = fetch_food_info("arroz")

    assert result is not None
    assert result["product_name"] == "Arroz Branco"
    assert result["brands"] == "Marca Teste"
    assert result["categories"] == "Cereais, Arroz"
    assert result["nutriscore"] == "A"
    # Garante que a aplicacao realmente chamou o endpoint da API publica.
    mock_get.assert_called_once()


@patch("src.api.requests.get")
def test_fetch_food_info_no_results(mock_get):
    """Quando a API nao retorna produtos, deve devolver None."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"products": []}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    assert fetch_food_info("xyzinexistente123") is None


@patch("src.api.requests.get")
def test_fetch_food_info_api_failure(mock_get):
    """Falha de rede/HTTP deve ser tratada e retornar None (sem quebrar)."""
    mock_get.side_effect = requests.RequestException("timeout")

    assert fetch_food_info("arroz") is None


def test_fetch_food_info_empty_item():
    """Item vazio nem chega a chamar a API."""
    assert fetch_food_info("") is None
    assert fetch_food_info("   ") is None
