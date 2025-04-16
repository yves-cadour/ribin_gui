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
    if 'last_upload' not in st.session_state:
        st.session_state.last_upload = None
    if 'seuil_effectif' not in st.session_state:
        st.session_state.seuil_effectif = 25
    if 'nb_specialites' not in st.session_state:
        st.session_state.nb_specialites = 3

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

def generate_menus(nb_barrettes, max_par_conflit_certain):
    """Génère les menus (appelé depuis sidebar)"""
    if not st.session_state.moulinette:
        raise ValueError("Moulinette non initialisée")
    moulinette = st.session_state.moulinette
    moulinette.nb_barrettes = nb_barrettes
    st.session_state.menus = moulinette.menus_tries_par_conflits_et_filtres(max_par_conflit_certain=5)
    st.session_state.current_menu_index = 0
