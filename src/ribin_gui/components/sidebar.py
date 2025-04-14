import streamlit as st
from ribin_gui.config.state import handle_upload

def sidebar():
    """Composition de la sidebar"""
    with st.sidebar:
        st.title("Navigation")
        display_navigation()

        if st.session_state.etape == 1:
            display_upload()
        elif st.session_state.etape == 2:
            display_groups()
        elif st.session_state.etape == 3:
            display_menus()


def display_navigation():
    """Affiche les boutons de navigation"""
    col1, col2 = st.columns(2)
    if st.session_state.etape > 1 and col1.button("← Retour"):
        st.session_state.etape -= 1

    disabled = st.session_state.etape >= 3 or not st.session_state.moulinette
    if col2.button("Suivant →", disabled=disabled):
        st.session_state.etape += 1

def display_upload():
    """Affiche le widget d'upload"""
    st.header("1. Données")
    uploaded_file = st.file_uploader("Importer CSV", type=["csv"])
    if uploaded_file and handle_upload(uploaded_file):
        st.success("Fichier importé !")
        st.rerun()

def display_groups():
    """Affiche la gestion des groupes"""
    st.header("2. Groupes")
    st.session_state.seuil_effectif = st.slider(
                "Seuil d'effectif pour mise en évidence",
                min_value=20,
                max_value=30,
                value=st.session_state.seuil_effectif,
                key="slider_effectif"
            )
    st.info(f"Les spécialités > {st.session_state.seuil_effectif} élèves sont mis en évidence.")

def display_menus():
    """Affiche la gestion des menus"""
    st.header("3. Menus")




