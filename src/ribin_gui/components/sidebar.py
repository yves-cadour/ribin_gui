import streamlit as st
import pandas as pd
from ribin.moulinette import Moulinette
from ribin_gui.config.state import reset_application_state, reset_menus, handle_upload_complete


def sidebar():
    with st.sidebar:
        _display_navigation_buttons()
        _handle_step_specific_content()

        # Gestion atomique de l'upload complet
        handle_upload_complete()

        # Single source of truth pour le rerun
        if st.session_state.get('file_just_uploaded', False):
            st.session_state.file_just_uploaded = False
            st.rerun()

def _display_navigation_buttons():
    """Affiche les boutons de navigation dans la barre latérale"""
    st.title("Navigation")
    col1, col2 = st.columns(2)
    texte_retour = "← Retour"
    texte_suivant = "Suivant →"
    # Bouton Retour
    if st.session_state.etape > 1:
        if col1.button(texte_retour, type="primary"):
            st.session_state.etape -= 1
            st.rerun()
    if st.session_state.etape < 3:
        # Désactivé seulement si moulinette n'existe pas ET aucun upload en cours
        disabled = not st.session_state.get('moulinette') and not st.session_state.get('upload_in_progress')
        if col2.button("Suivant →", disabled=disabled, type="primary"):
            st.session_state.etape += 1

def _handle_step_specific_content():
    """Affiche le contenu spécifique à chaque étape dans la barre latérale"""
    if st.session_state.etape == 1:
        _display_handle_datas()
    elif st.session_state.etape == 2:
        _display_handle_groups()
    elif st.session_state.etape == 3:
        _display_handle_menus()

def _display_handle_datas():
    st.header("1. Données")
    uploaded_file = st.file_uploader("Importer CSV", type=["csv"])

    if uploaded_file:
        reset_application_state()
        st.session_state.moulinette = Moulinette()
        df = pd.read_csv(uploaded_file)
        st.session_state.moulinette.read_datas(df)
        st.success("Fichier importé !")
        st.session_state.upload_in_progress = True  # Marque le début de l'upload

def _display_handle_groups():
    """Affiche, dans la barre latérale, le contenu spécifique à l'étape 2 (gestion des groupes)"""
    st.header("2. Gestion des groupes")

def _display_handle_menus():
    """Affiche, dans la barre latérale, le contenu spécifique à l'étape 3 (génération des menus)"""
    st.header("3. Détermination du nombre de barrettes")
    nb_barrettes = st.slider("Nombre de barrettes",
                                min_value=2,
                                max_value=5,
                                value=st.session_state.moulinette.nb_barrettes,
                                on_change=reset_menus)
    if st.session_state.moulinette:
        st.session_state.moulinette.nb_barrettes = nb_barrettes
        # Réinitialiser les conflits quand on change le nombre de barrettes
        reset_menus(origine="slider nb barrettes")

    if st.button("🎯 Générer les menus", type="primary"):
        with st.spinner("Génération en cours..."):
            st.session_state.menus = st.session_state.moulinette.menus_tries_par_conflits_et_filtres(max_par_conflit_certain=5)
            st.session_state.current_menu_index = 0
            st.rerun()

