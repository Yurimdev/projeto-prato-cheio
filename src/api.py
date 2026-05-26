from __future__ import annotations

import requests

OPEN_FOOD_FACTS_URL = "https://world.openfoodfacts.org/cgi/search.pl"


def fetch_food_info(item_name: str, timeout: int = 10) -> dict | None:
    """Consulta a API publica Open Food Facts e retorna dados do alimento.

    Recebe o nome de um item doado e busca informacoes complementares
    (marca, categoria e Nutri-Score) para enriquecer o cadastro.
    Retorna None quando a API falha ou nao encontra o produto.
    """
    if not item_name or not item_name.strip():
        return None

    params = {
        "search_terms": item_name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1,
    }

    try:
        response = requests.get(
            OPEN_FOOD_FACTS_URL, params=params, timeout=timeout
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return None

    products = data.get("products", [])
    if not products:
        return None

    product = products[0]
    return {
        "product_name": product.get("product_name") or item_name,
        "brands": product.get("brands") or "Desconhecida",
        "categories": product.get("categories") or "Nao classificado",
        "nutriscore": (product.get("nutriscore_grade") or "n/d").upper(),
    }
