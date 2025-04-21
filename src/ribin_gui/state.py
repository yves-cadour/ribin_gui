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
        'uploaded_file': None,

        # Groupes
        'seuil_effectif': 24,

        # Menus
        'menus': None,
        'current_menu_index': None,
        'nb_barrettes': None,
        'selected_menu' : None,
    }

    @classmethod
    def init(cls):
        """Initialise tous les états nécessaires"""
        for key, default in cls._DEFAULTS.items():
            st.session_state.setdefault(key, default)

    @classmethod
    def get(cls, key: str, expected_type: Optional[type] = None) -> Any:
        """Récupère une valeur de la session avec vérification de type"""
        value = st.session_state.get(key, cls._DEFAULTS.get(key))

        if expected_type and not isinstance(value, expected_type):
            raise TypeError(f"{key} doit être de type {expected_type}, a reçu {type(value)}")
        return value

    @classmethod
    def update(cls, key: str, value: Any) -> bool:
        """Met à jour une valeur seulement si elle a changé"""
        current = cls.get(key)
        if current != value:
            st.session_state[key] = value
            return True
        return False


# Fonction d'initialisation pour compatibilité ascendante
def init_state():
    """
    Initialisation de tous les états de la session
    """
    AppState.init()
