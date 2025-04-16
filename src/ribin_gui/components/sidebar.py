import streamlit as st
from ribin_gui.config.state import handle_upload, generate_menus

def sidebar():
    """Composition de la sidebar"""
    with st.sidebar:
        st.title("Navigation")
        display_navigation()

        if st.session_state.etape == 1:
            display_nb_specialites()
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

def display_nb_specialites():
    """
    Affiche le slider pour le choix du nombre de spécialités par éléève.
    """
    st.session_state.nb_specialites = st.slider(
                "Nombre de spécialités par élève",
                min_value=2,
                max_value=3,
                value=st.session_state.nb_specialites,
                key="slider_nb_specialites"
            )
    st.info(f"3 spécialités en première, 2 en terminale.")

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
    max_conflits_certains = st.slider("Maximum de conflits certains",
                                    min_value=1,
                                    max_value=10,
                                    value=st.session_state.moulinette.nb_barrettes,
                            key="nb_barrettes_slider")

    nb_barrettes = st.slider("Nombre de barrettes",
                            min_value=2,
                            max_value=5,
                            value=st.session_state.moulinette.nb_barrettes,
                            key="nb_barrettes_slider")
    if st.button("🎯 Générer les menus", type="primary", key="generate_menus"):
       with st.spinner("Génération en cours..."):
            try:
                generate_menus(nb_barrettes)
                st.success("Menus générés avec succès!")
            except ValueError as e:
                st.error(f"Erreur lors de la génération des menus : {e}")




