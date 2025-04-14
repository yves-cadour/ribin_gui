import streamlit as st
from ribin_gui.config.state import handle_upload


def display_upload():
    """Affiche le widget d'upload"""
    uploaded_file = st.file_uploader("Importer CSV", type=["csv"])
    if uploaded_file and handle_upload(uploaded_file):
        st.success("Fichier importé !")

def display_navigation():
    """Affiche les boutons de navigation"""
    col1, col2 = st.columns(2)
    if st.session_state.etape > 1 and col1.button("← Retour"):
        st.session_state.etape -= 1

    disabled = st.session_state.etape >= 3 or not st.session_state.moulinette
    if col2.button("Suivant →", disabled=disabled):
        st.session_state.etape += 1

def sidebar():
    """Composition de la sidebar"""
    with st.sidebar:
        st.title("Navigation")
        display_navigation()

        if st.session_state.etape == 1:
            st.header("1. Données")
            display_upload()