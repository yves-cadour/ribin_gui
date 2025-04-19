"""Le contrôleur de la vue sidebar"""

import pandas as pd
from ribin import Moulinette
import streamlit as st
from ribin_gui.state import AppState
from ribin_gui.controllers.main_controller import MainController


class SidebarController:
    """
    Une classe pour le contrôleur de la barre latérale
    """

    # +-----------------------------------------------------------+
    # |            etape 1 (importation des données)              |
    # +-----------------------------------------------------------+
    @staticmethod
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
        if AppState.update('nb_specialites', nb_specialites):
            AppState.update('moulinette', None)
            return True
        return False

    @staticmethod
    def get_uploaded_file()->bool:
        """Retourne la valeur du fichier téléversé (bytes)
        :return: True si changement, False sinon
        :rtype: bool
        """
        return AppState.get('uploaded_file')

    @staticmethod
    def update_uploaded_file(new_uploaded_file, new_uploaded_file_value)->bool:
        """Met à jour la valeur du fichier téléversé. Si celle-ci a changé, retourne True sinon False.

        :param new_value: la valeur venant du widget
        :type new_value: ?
        :return: True si changement, False sinon
        :rtype: bool
        """
        if AppState.update('uploaded_file', new_uploaded_file_value):
            try:
                AppState.update('moulinette', None) # necessaire pour maj de la vue des données
                nb_specialites = AppState.get('nb_specialites', int)
                moulinette = Moulinette()
                moulinette.nb_specialites = nb_specialites

                df = pd.read_csv(new_uploaded_file)
                moulinette.read_datas(df)

                AppState.update('moulinette', moulinette)
                return True

            except pd.errors.EmptyDataError:
                st.error("Le fichier est vide")
            except pd.errors.ParserError:
                st.error("Format de fichier invalide")
            except Exception as e:
                st.error(f"Erreur technique: {str(e)}")
                AppState.update('moulinette', None)

        return False

    # +-----------------------------------------------------------+
    # |            etape 2 (gestion des groupes)                  |
    # +-----------------------------------------------------------+

    @staticmethod
    def get_seuil_effectif()->int:
        """Retourne le seuil effectif de la session.

        :return: la valeur du seuil
        :rtype: int
        """
        return AppState.get('seuil_effectif', int)

    @staticmethod
    def update_seuil_effectif(new_value:int)->bool:
        """Met à jour la valeur du seuil. Si celle-ci a changé, retourne True sinon False.

        :param new_value: la valeur venant du widget
        :type new_value: int
        :return: True si changement, False sinon
        :rtype: bool
        """
        return AppState.update('seuil_effectif', new_value)

    # +-----------------------------------------------------------+
    # |            etape 3 (gestion des menus)                    |
    # +-----------------------------------------------------------+

    @staticmethod
    def update_nb_barrettes(new_value:int)->bool:
        """Met à jour le nombre de barrettes dans la moulinette

        :param new_value: la nouvelle valeur.
        :type new_value: int
        :return: True si la valeur a changé, False sinon.
        :rtype: bool
        """
        moulinette = MainController.get_moulinette()
        if moulinette.nb_barrettes != new_value:
            moulinette.nb_barrettes = new_value
            MainController.reset_menus()
            return True
        return False

    @staticmethod
    def update_max_conflits(new_value:int, conflict_type: str)->bool:
        """Met à jour les conflits.

        :param new_value: la nouvelle valeur.
        :type new_value: int
        :param conflict_type: Types possibles: 'insolubles' ou 'potentiels'.
        :type new_value: int
        :return: True si la valeur a changé, False sinon.
        :rtype: bool
        """
        moulinette = MainController.get_moulinette()

        if conflict_type == 'insolubles':
            attr = 'max_conflits_certains'
        elif conflict_type == 'potentiels':
            attr = 'max_conflits_potentiels_par_conflit_certain'
        else:
            raise ValueError("Type de conflit invalide")

        if getattr(moulinette, attr) != new_value:
            setattr(moulinette, attr, new_value)
            MainController.reset_menus()
            return True
        return False
