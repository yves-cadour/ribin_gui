"""Le contrôleur principal"""

import streamlit as st

def get_moulinette():
    """Retourne la moulinette de la session
    """
    return st.session_state.moulinette
