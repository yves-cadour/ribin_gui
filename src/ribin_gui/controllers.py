"""Les controleurs"""


import streamlit as st
import pandas as pd
from ribin.moulinette import Moulinette
from .state import reset_menus


# +-----------------------------------------------------------+
# |           1 : CONTROLEUR DES DONNEES                      |
# +-----------------------------------------------------------+

def handle_upload(uploaded_file):
    """Gère un nouvel upload de fichier"""
    if uploaded_file:
        try:
            # Initialisation de la moulinette (Modèle)
            st.session_state.moulinette = Moulinette()
            st.session_state.nb_specialites = st.session_state.moulinette.nb_specialites

            # Lecture des données
            df = pd.read_csv(uploaded_file)
            st.session_state.moulinette.read_datas(df)
            return True
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier: {e}")
            return False
    return False

# +-----------------------------------------------------------+
# |           2 : CONTROLEUR DES GROUPES                      |
# +-----------------------------------------------------------+

# +-----------------------------------------------------------+
# |           3 : CONTROLEUR DES MENUS                        |
# +-----------------------------------------------------------+

def generate_menus():
    """Génération des menus et affectation dans st.session_state.menus"""
    if not st.session_state.moulinette:
        raise ValueError("Moulinette non initialisée")
    reset_menus()
    try:
        st.session_state.menus = st.session_state.moulinette.menus_tries_par_conflits_et_filtres()
        st.session_state.current_menu_index = 0
        return True
    except Exception as e:
        reset_menus()
        raise e
