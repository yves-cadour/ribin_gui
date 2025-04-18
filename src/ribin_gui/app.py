"""Le point d'entrée de l'application"""

import streamlit as st
from ribin_gui.state import init_state
from ribin_gui.views import sidebar_view, datas_view, groups_view, menus_view

def config_page():
    """
    Configuration globale de la page
    """
    st.set_page_config(layout="wide", page_title="Gestion des menus de spécialités")
    st.markdown("""
    <style>
        .sidebar .stButton>button { width: 100%; margin: 5px 0; }
        div[data-testid="stExpander"] div[role="button"] p { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)


def main():
    """Le point d'entrée de l'application"""
    init_state()
    config_page()
    sidebar_view.render()

    # Router vers la vue appropriée
    if st.session_state.etape == 1:
        datas_view.render()
    elif st.session_state.etape == 2:
        groups_view.render()
    elif st.session_state.etape == 3:
        menus_view.render()

if __name__ == "__main__":
    main()