def validate_quantity(quantity: int) -> bool:
    """
    Valida se a quantidade doada é um número inteiro positivo.
    Não permite valores negativos ou zero.
    """
    if not isinstance(quantity, int):
        return False
    return quantity > 0

def format_donation_entry(donor: str, item: str, quantity: int) -> dict:
    """
    Formata os dados da doação em um dicionário estruturado.
    """
    return {
        "donor": donor.strip(),
        "item": item.strip(),
        "quantity": quantity
    }
