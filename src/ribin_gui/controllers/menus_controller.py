"""Le contrôleur de la vue des menus"""

import streamlit as st

from ribin_gui.controllers import main_controller

def current_menu_index()->int:
    """
    Retourne la valeur de l'index du menu courant.

    :return: la valeur de l'index du menu courant
    :rtype: int
    """
    return st.session_state.current_menu_index

def incremente_menu_index()->int:
    """Incrémente la valeur de l'index du menu courant.

    :return: la nouvelle valeur de l'index du menu courant.
    :rtype: int
    """
    if current_menu_index() < len(main_controller.get_menus())-1:
        st.session_state.current_menu_index += 1
    return current_menu_index()

def decremente_menu_index()->int:
    """Décrémente la valeur de l'index du menu courant.

    :return: la nouvelle valeur de l'index du menu courant.
    :rtype: int
    """
    if current_menu_index() > 0:
        st.session_state.current_menu_index -= 1
    return current_menu_index()

