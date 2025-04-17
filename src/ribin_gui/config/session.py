import streamlit as st


def init_session():
    """Initialise tous les états de session"""
    defaults = {
        'etape': 1,
        'current_menu_index': 0,
        'seuil_effectif': 24,
        'moulinette': None,
        'menus': None,
        'nb_barrettes': None,
        'nb_specialites': None,
        'max_conflits_certains': None,
        'max_conflits_potentiels': None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_menus():
    """Réinitialise complètement la génération des menus"""
    if st.session_state.moulinette:
        st.session_state.moulinette.reset_menus()
        st.session_state.current_menu_index = 0

