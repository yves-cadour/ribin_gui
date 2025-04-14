import streamlit as st

# Configuration de la page
def config_page():
    st.set_page_config(layout="wide", page_title="Gestion des menus de spécialités")
    st.markdown("""
    <style>
        .sidebar .stButton>button { width: 100%; margin: 5px 0; }
        div[data-testid="stExpander"] div[role="button"] p { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)
