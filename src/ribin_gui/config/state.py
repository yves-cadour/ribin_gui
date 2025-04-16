import streamlit as st
import pandas as pd
from ribin.moulinette import Moulinette

# +-----------------------------------------------------------------------+
# |      state.py                                                         |
# |      - Gère toute la logique métier                                   |
# |      - Modifie le state global                                        |
# |      - Ne contient aucun élément d'UI                                 |
# +-----------------------------------------------------------------------+

def init_state():
    """Initialise tous les états nécessaires"""
    if 'etape' not in st.session_state:
        st.session_state.etape = 1
    if 'moulinette' not in st.session_state:
        st.session_state.moulinette = None
    if 'menus' not in st.session_state:
        st.session_state.menus = None
    if 'last_upload' not in st.session_state:
        st.session_state.last_upload = None
    if 'current_menu_index' not in st.session_state:
        st.session_state.current_menu_index = None
    if 'seuil_effectif' not in st.session_state:
        st.session_state.seuil_effectif = 24
    if 'nb_specialites' not in st.session_state:
        st.session_state.nb_specialites = None
    if 'nb_barrettes' not in st.session_state:
        st.session_state.nb_barrettes = None
    if 'max_conflits_certains' not in st.session_state:
        st.session_state.max_conflits_certains = None
    if 'max_conflits_potentiels_par_conflit_certain' not in st.session_state:
        st.session_state.max_conflits_potentiels_par_conflit_certain = None

def handle_upload(uploaded_file):
    """Gère un nouvel upload de fichier"""
    if uploaded_file and st.session_state.last_upload != uploaded_file.name:
        st.session_state.moulinette = Moulinette()
        st.session_state.moulinette.nb_specialites = st.session_state.nb_specialites
        df = pd.read_csv(uploaded_file)
        st.session_state.moulinette.read_datas(df)
        st.session_state.last_upload = uploaded_file.name
        return True
    return False

def handle_nb_specialites_par_eleve():
    """Retourne vrai si l'instance de la moulinette existe.
    """
    if st.session_state.moulinette is not None:
        return True
    return False

def generate_menus():
    if not st.session_state.moulinette:
        raise ValueError("Moulinette non initialisée")

    moulinette = st.session_state.moulinette

    # Réinitialisation complète
#    moulinette._menus = None  # Force la regénération

    # Synchronisation explicite
    moulinette.nb_barrettes = st.session_state.nb_barrettes
    moulinette.max_conflits_certains = st.session_state.max_conflits_certains
    moulinette.max_conflits_potentiels_par_conflit_certain = st.session_state.max_conflits_potentiels_par_conflit_certain

    # Génération et vérification
    menus = moulinette.menus_tries_par_conflits_et_filtres()

    # Validation critique
    if menus and len(menus[0].barrettes) != moulinette.nb_barrettes:
        raise ValueError(f"Incohérence détectée: {len(menus[0].barrettes)} barrettes au lieu de {moulinette.nb_barrettes}")

    st.session_state.menus = menus
    st.session_state.current_menu_index = 0
    st.rerun()  # Force le rafraîchissement complet
