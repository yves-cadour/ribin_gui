"""Gestion centralisée de l'état global de l'application"""

from typing import Any, Optional
import streamlit as st

class AppState:
    """Classe encapsulant l'état de l'application"""

    # Définition des clés avec valeurs par défaut
    _DEFAULTS = {
        # Navigation
        'etape': 1,
        'nb_etapes': 4,

        # Données
        'nb_specialites': 3,
        'moulinette': None,

        # Groupes
        'seuil_effectif': 24,

        # Menus
        'menus': None,
        'current_menu_index': None,
        'nb_barrettes': None
    }

    @classmethod
    def init(cls):
        """Initialise tous les états nécessaires"""
        for key, default in cls._DEFAULTS.items():
            st.session_state.setdefault(key, default)


# Fonction d'initialisation pour compatibilité ascendante
def init_state():
    """
    Initialisation de tous les états de la session
    """
    AppState.init()
