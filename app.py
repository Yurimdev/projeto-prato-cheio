import streamlit as st

from src.utils import validate_quantity, format_donation_entry
from src.api import fetch_food_info

st.set_page_config(
    page_title="Prato Cheio",
    layout="centered",
    initial_sidebar_state="collapsed",
)

CSS = """
<style>
#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 2.5rem; max-width: 760px;}

.pc-header {
    border-left: 5px solid #2e7d32;
    padding: 0.2rem 0 0.2rem 1rem;
    margin-bottom: 1.8rem;
}
.pc-header h1 {
    font-size: 1.9rem;
    font-weight: 700;
    margin: 0;
    color: #1b3a2b;
    letter-spacing: -0.3px;
}
.pc-header p {
    margin: 0.35rem 0 0;
    color: #5f6b63;
    font-size: 0.95rem;
}

.pc-section-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #1b3a2b;
    margin: 1.6rem 0 0.6rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #e2e6e3;
}

.stButton > button {
    background-color: #2e7d32;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 0.45rem 1.4rem;
    font-weight: 600;
}
.stButton > button:hover {
    background-color: #256528;
    color: #ffffff;
}

.pc-item {
    border: 1px solid #e2e6e3;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    background: #fafbfa;
}
.pc-item .pc-title {font-weight: 600; color: #1b3a2b;}
.pc-item .pc-meta {color: #5f6b63; font-size: 0.88rem; margin-top: 0.25rem;}

/* Campos de entrada com borda visivel */
div[data-baseweb="input"],
div[data-baseweb="base-input"] {
    background-color: #ffffff !important;
    border: 1.6px solid #2e7d32 !important;
    border-radius: 6px !important;
}
div[data-baseweb="input"] input {
    background-color: #ffffff !important;
    color: #1b2620 !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #1b5e20 !important;
    box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.20) !important;
}
.stTextInput label, .stNumberInput label {
    font-weight: 600 !important;
    color: #1b3a2b !important;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

if "donations" not in st.session_state:
    st.session_state.donations = []

st.markdown(
    """
    <div class="pc-header">
        <h1>Projeto Prato Cheio</h1>
        <p>Gestão de doações para bancos de alimentos, com consulta de
        informações de produtos na API pública Open Food Facts.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="pc-section-title">Registrar doação</div>',
            unsafe_allow_html=True)

with st.form("add_donation", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        donor = st.text_input("Doador")
        item = st.text_input("Item doado")
    with col2:
        qty = st.number_input("Quantidade", min_value=1, step=1, value=1)
    enrich = st.checkbox(
        "Buscar dados do produto na Open Food Facts", value=True
    )
    submitted = st.form_submit_button("Registrar doação")

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
                    f"Doação registrada. Categoria: {info['categories']} | "
                    f"Nutri-Score: {info['nutriscore']}"
                )
            else:
                st.warning(
                    "Doação registrada, mas a API não retornou dados para "
                    "este item."
                )
        else:
            st.success("Doação registrada.")
        st.session_state.donations.append(entry)

st.markdown('<div class="pc-section-title">Estoque de doações</div>',
            unsafe_allow_html=True)

if not st.session_state.donations:
    st.caption("Nenhuma doação registrada ainda.")
else:
    total = sum(d["quantity"] for d in st.session_state.donations)
    st.caption(
        f"{len(st.session_state.donations)} registro(s) | "
        f"{total} item(ns) no total."
    )
    for idx, d in enumerate(st.session_state.donations, 1):
        meta = f"Doador: {d['donor']}"
        info = d.get("info")
        if info:
            meta += (
                f" &nbsp;|&nbsp; Marca: {info['brands']}"
                f" &nbsp;|&nbsp; Categoria: {info['categories']}"
                f" &nbsp;|&nbsp; Nutri-Score: {info['nutriscore']}"
            )
        st.markdown(
            f"""
            <div class="pc-item">
                <div class="pc-title">{idx}. {d['item']} — {d['quantity']}x</div>
                <div class="pc-meta">{meta}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
