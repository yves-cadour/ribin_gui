import streamlit as st
from ..config.session import reset_menus

def generate_menus():
    if not st.session_state.moulinette:
        raise ValueError("Moulinette non initialisée")
    reset_menus()
    moulinette = st.session_state.moulinette
    moulinette.nb_barrettes = st.session_state.nb_barrettes
    try:
        st.session_state.menus = moulinette.menus_tries_par_conflits_et_filtres()
        validate_menus()  # Validation supplémentaire
        return True
    except Exception as e:
        reset_menus()
        raise e

def validate_menus():
    """Valide la cohérence des menus générés"""
    if not st.session_state.menus:
        return

    expected = st.session_state.nb_barrettes
    actual = len(st.session_state.menus[0].barrettes)

    if actual != expected:
        reset_menus()
        raise ValueError(f"Incohérence détectée: {actual} barrettes au lieu de {expected}")