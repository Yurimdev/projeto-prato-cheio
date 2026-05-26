import streamlit as st

from src.utils import validate_quantity, format_donation_entry
from src.api import fetch_food_info

st.set_page_config(page_title="Prato Cheio", page_icon="🍽️", layout="centered")

if "donations" not in st.session_state:
    st.session_state.donations = []

st.title("🍽️ Projeto Prato Cheio")
st.caption(
    "Gestão de doações para bancos de alimentos — com dados de alimentos "
    "via API pública Open Food Facts."
)

st.header("➕ Registrar doação")
with st.form("add_donation", clear_on_submit=True):
    donor = st.text_input("Doador")
    item = st.text_input("Item doado")
    qty = st.number_input("Quantidade", min_value=1, step=1, value=1)
    enrich = st.checkbox(
        "Buscar dados do alimento na API Open Food Facts", value=True
    )
    submitted = st.form_submit_button("Registrar")

if submitted:
    if not donor.strip() or not item.strip():
        st.error("Doador e item não podem ser vazios.")
    elif not validate_quantity(int(qty)):
        st.error("A quantidade deve ser um inteiro maior que zero.")
    else:
        entry = format_donation_entry(donor, item, int(qty))
        if enrich:
            with st.spinner("Consultando Open Food Facts..."):
                info = fetch_food_info(item)
            if info:
                entry["info"] = info
                st.success(
                    f"Doação registrada! Categoria detectada: "
                    f"{info['categories']} | Nutri-Score: {info['nutriscore']}"
                )
            else:
                st.warning(
                    "Doação registrada, mas a API não retornou dados para "
                    "este item."
                )
        else:
            st.success("Doação registrada!")
        st.session_state.donations.append(entry)

st.header("📋 Estoque de doações")
if not st.session_state.donations:
    st.info("Nenhuma doação registrada ainda.")
else:
    for idx, d in enumerate(st.session_state.donations, 1):
        line = f"**{idx}. {d['item']}** — {d['quantity']}x (Doador: {d['donor']})"
        info = d.get("info")
        if info:
            line += (
                f"  \n↳ Marca: {info['brands']} | "
                f"Categoria: {info['categories']} | "
                f"Nutri-Score: {info['nutriscore']}"
            )
        st.markdown(line)
