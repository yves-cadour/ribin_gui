"""Gestion des états"""

import streamlit as st

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
    # moulinette
    if 'moulinette' not in st.session_state:
        st.session_state.moulinette = None
    if 'nb_specialites' not in st.session_state:
        st.session_state.nb_specialites = None
    # menus
    if 'menus' not in st.session_state:
        st.session_state.menus = None
    if 'current_menu_index' not in st.session_state:
        st.session_state.current_menu_index = None
    if 'nb_barrettes' not in st.session_state:
        st.session_state.nb_barrettes = None
    if 'max_conflits_certains' not in st.session_state:
        st.session_state.max_conflits_certains = None
    if 'max_conflits_potentiels_par_conflit_certain' not in st.session_state:
        st.session_state.max_conflits_potentiels_par_conflit_certain = None
    # groupes
    if 'seuil_effectif' not in st.session_state:
        st.session_state.seuil_effectif = 24
    # resolver
    if 'conflict_resolver' not in st.session_state:
        st.session_state.conflict_resolver = None

def reset_menus():
    """Réinitialise les menus_
    """
    st.session_state.moulinette.reset_menus()
    st.session_state.menus = None
    st.session_state.current_menu_index = None

