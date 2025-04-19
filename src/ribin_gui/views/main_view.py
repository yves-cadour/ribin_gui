"""La vue des principale"""

import streamlit as st
from ..views import sidebar_view, datas_view, groups_view, menus_view
from ..controllers.main_controller import MainController

def render():
    """
    La vue principale de la page
    """
    st.set_page_config(layout="wide", page_title="Gestion des menus de spécialités")
    st.markdown("""
    <style>
        *  {font-size : 15px !important}
        h1 { font-size: 25px !important}
        h2 { font-size: 20px !important}
        h3 { font-size: 17px !important}
        .st-emotion-cache-t1wise {padding : 20px !important}
    </style>
    """, unsafe_allow_html=True)
    # la barre latérale
    sidebar_view.render()

    # affichage des vues selon l'étape
    etape = MainController.get_etape()
    if etape == 1:
        datas_view.render()
    elif etape == 2:
        groups_view.render()
    elif etape == 3:
        menus_view.render()
