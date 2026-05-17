import requests

def validate_quantity(quantity: int) -> bool:
    """
    Valida se a quantidade doada é um número inteiro positivo.
    Não permite valores negativos ou zero.
    """
    if not isinstance(quantity, int):
        return False
    return quantity > 0

def fetch_address_from_cep(cep: str) -> str:
    """Busca a cidade e estado a partir do CEP via API do ViaCEP."""
    if not cep:
        return "Local não informado"
    
    cep_digits = ''.join(filter(str.isdigit, cep))
    if len(cep_digits) != 8:
        return "CEP inválido"
        
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep_digits}/json/", timeout=5)
        response.raise_for_status()
        data = response.json()
        if "erro" in data:
            return "CEP não encontrado"
        return f"{data.get('localidade', '')} - {data.get('uf', '')}"
    except requests.RequestException:
        return "Erro ao buscar CEP"

def format_donation_entry(donor: str, item: str, quantity: int, cep: str = None) -> dict:
    """
    Formata os dados da doação em um dicionário estruturado, incluindo localização.
    """
    address = fetch_address_from_cep(cep) if cep else "Local não informado"
    return {
        "donor": donor.strip(),
        "item": item.strip(),
        "quantity": quantity,
        "location": address
    }
