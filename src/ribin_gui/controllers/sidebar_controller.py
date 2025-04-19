"""Le contrôleur de la vue sidebar"""

import pandas as pd
from ribin import Moulinette
import streamlit as st

from ribin_gui.controllers import main_controller
# +-----------------------------------------------------------+
# |           CONTROLEUR DE LA VUE 'SIDEBAR'                  |
# +-----------------------------------------------------------+


# +-----------------------------------------------------------+
# |            etape 1 (importation des données)              |
# +-----------------------------------------------------------+

def update_nb_specialites(nb_specialites:int)->bool:
    """
    Met à jour le nombre de spécialités par élève dans la session.
    Si le nombre a changé, réinitialise la moulinette et renvoie Vrai, sinon renvoie False.

    :param nb_specialites: Le nombre de spécialités par élève.
    :type nb_specialites: int
    :raises ValueError: si 'moulinette' ou 'nb_specialites' absent de la session.
    :return: Vrai si changement, Faux sinon.
    :rtype: bool
    """
    for key in ['moulinette','nb_specialites']:
        if key not in st.session_state:
            raise ValueError(f"'{key}' n'est pas présent dans la session.")
    if st.session_state.nb_specialites != nb_specialites:
        st.session_state.nb_specialites = nb_specialites
        return True
    return False

def handle_upload(uploaded_file)->bool:
    """Creer la moulinette depuis les données importées

    :param uploaded_file: le fichier csv
    :type uploaded_file:?
    :raises ValueError: si 'moulinette' ou 'nb_specialites' absent de la session.
    :return: vrai l'import du fichier a réussi, faux sinon.
    :rtype: bool
    """
    if uploaded_file:

        for key in ['moulinette','nb_specialites']:
            if key not in st.session_state:
                raise ValueError(f"'{key}' n'est pas présent dans la session.")
        try:
            st.session_state.moulinette = Moulinette()
            st.session_state.moulinette.nb_specialites = st.session_state.nb_specialites
            # Lecture des données
            df = pd.read_csv(uploaded_file)
            st.session_state.moulinette.read_datas(df)
            return True
        except Exception as e:
            st.session_state.moulinette = None
            #st.session_state.nb_specialites = 3
            #print("handle_upload -> st.session_state.nb_specialites = 3")
            st.error(f"Erreur lors de la lecture du fichier: {e}")
            return False
    return False

# +-----------------------------------------------------------+
# |            etape 2 (gestion des groupes)                  |
# +-----------------------------------------------------------+

def get_seuil_effectif()->int:
    """Retourne le seuil effectif de la session.

    :return: la valeur du seuil
    :rtype: int
    """
    return st.session_state.seuil_effectif

def update_seuil_effectif(new_value:int)->bool:
    """Met à jour la valeur du seuil. Si celle-ci a changé, retourne True sinon False.

    :param new_value: la valeur venant du widget
    :type new_value: int
    :return: True si changement, False sinon
    :rtype: bool
    """
    if new_value != get_seuil_effectif():
        st.session_state.seuil_effectif = new_value
        return True
    return False

# +-----------------------------------------------------------+
# |            etape 3 (gestion des menus)                    |
# +-----------------------------------------------------------+

def update_nb_barrettes(new_value:int)->bool:
    """Met à jour le nombre de barrettes dans la moulinette

    :param new_value: la nouvelle valeur.
    :type new_value: int
    :return: True si la valeur a changé, False sinon.
    :rtype: bool
    """
    moulinette = main_controller.get_moulinette()
    if moulinette.nb_barrettes != new_value:
        moulinette.nb_barrettes = new_value
        main_controller.reset_menus()
        return True
    return False

def update_max_conflits_certains(new_value:int)->bool:
    """Met à jour le nombre maxium de conflits insolubles à afficher.

    :param new_value: la nouvelle valeur.
    :type new_value: int
    :return: True si la valeur a changé, False sinon.
    :rtype: bool
    """
    moulinette = main_controller.get_moulinette()
    if moulinette.max_conflits_certains != new_value:
        moulinette.max_conflits_certains = new_value
        main_controller.reset_menus()
        return True
    return False

def update_max_conflits_potentiels(new_value:int)->bool:
    """Met à jour le nombre maxium de conflits potentiels (par conflit insoluble) à afficher.

    :param new_value: la nouvelle valeur.
    :type new_value: int
    :return: True si la valeur a changé, False sinon.
    :rtype: bool
    """
    moulinette = main_controller.get_moulinette()
    if moulinette.max_conflits_potentiels_par_conflit_certain != new_value:
        moulinette.max_conflits_potentiels_par_conflit_certain = new_value
        main_controller.reset_menus()
        return True
    return False
