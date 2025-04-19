"""Gestion des états"""

import streamlit as st

# +-----------------------------------------------------------------------+
# |      state.py                                                         |
# |      - Modifie le state global                                        |
# |      - Ne contient aucun élément d'UI                                 |
# +-----------------------------------------------------------------------+

def init_state():
    """Initialise tous les états nécessaires"""

    # ------------- NAVIGATION
    st.session_state.setdefault('etape', 1)

    # ------------- IMPORTATION DES DONNEES

    # nb_specialites -> valeur à déterminer dans la gui avant l'importation des données
    st.session_state.setdefault('nb_specialites', 3)

    # moulinette
    st.session_state.setdefault('moulinette', None)

    # ------------- CREATION DES GROUPES

    # groupes
    st.session_state.setdefault('seuil_effectif', 24)

    # ------------- CREATION DES MENUS

    # menus
    st.session_state.setdefault('menus', None)
    st.session_state.setdefault('current_menu_index', None)
    st.session_state.setdefault('nb_barrettes', None)

def reset_menus():
    """Réinitialise les menus_
    """
    st.session_state.moulinette.reset_menus()
    st.session_state.menus = None
    st.session_state.current_menu_index = None

