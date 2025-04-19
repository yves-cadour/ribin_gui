"""Le contrôleur principal"""

from typing import List
import streamlit as st
from ribin.interfaces import _IMoulinette, _IMenu

def get_moulinette()->_IMoulinette:
    """
    Retourne la moulinette de la session.
    """
    return st.session_state.moulinette

def get_nb_etapes()->int:
    """
    Retourne le nombre d'étapes.

    :return: le nombre d'étapes.
    :rtype: int
    """
    return st.session_state.get('nb_etapes')

def get_etape()->int:
    """
    Retourne le numéro de l'étape de la session.

    :return: le numéro de l'étape.
    :rtype: int
    """
    return st.session_state.get('etape')

def incrementer_etape()->int:
    """
    Incrémente le numéro de l'étape et retourne la nouvelle valeur.

    :return: le nouveau numéro d'étape.
    :rtype: int
    """
    st.session_state.etape += 1
    return get_etape()

def decrementer_etape()->int:
    """
    Décrémente le numéro de l'étape et retourne la nouvelle valeur.

    :return: le nouveau numéro d'étape.
    :rtype: int
    """

    if get_etape() > 1:
        st.session_state.etape -= 1
    return get_etape()


def generer_menus()->None:
    """
    Génère les menus de la moulinette.
    """
    menus = get_moulinette().menus_tries_par_conflits_et_filtres()
    st.session_state.menus = menus
    st.session_state.current_menu_index = 0

def get_menus()->List[_IMenu]:
    """Retourne les menus de la session.

    :return:Les menus
    :rtype: List[_IMenu]
    """
    return st.session_state.menus

def reset_menus()->None:
    """
    Réinitialise les menus.
    """
    st.session_state.moulinette.reset_menus()
    st.session_state.menus = None
    st.session_state.current_menu_index = None
