"""Le contrôleur principal"""

from typing import List
from ribin.interfaces import _IMoulinette, _IMenu
from ribin_gui.state import AppState

class MainController:
    """
    Une classe pour le contrôleur principal
    """

    @staticmethod
    def get_moulinette()->_IMoulinette:
        """
        Retourne la moulinette de la session.
        """
        moulinette = AppState.get('moulinette')
        #if moulinette is None:
        #    raise ValueError("La moulinette n'a pas été initialisée")
        return moulinette

    @staticmethod
    def get_nb_etapes()->int:
        """
        Retourne le nombre d'étapes.

        :return: le nombre d'étapes.
        :rtype: int
        """
        return AppState.get('nb_etapes', int)

    @staticmethod
    def get_etape()->int:
        """
        Retourne le numéro de l'étape de la session.

        :return: le numéro de l'étape.
        :rtype: int
        """
        return AppState.get('etape', int)

    @staticmethod
    def incrementer_etape()->int:
        """
        Incrémente le numéro de l'étape et retourne la nouvelle valeur.

        :return: le nouveau numéro d'étape.
        :rtype: int
        """
        current = MainController.get_etape()
        max_etapes = MainController.get_nb_etapes()
        if current < max_etapes:
            AppState.update('etape', current + 1)
        return MainController.get_etape()

    @staticmethod
    def decrementer_etape()->int:
        """
        Décrémente le numéro de l'étape et retourne la nouvelle valeur.

        :return: le nouveau numéro d'étape.
        :rtype: int
        """
        current = MainController.get_etape()
        if current > 1:
            AppState.update('etape', current - 1)
        return MainController.get_etape()

    @staticmethod
    def generer_menus()->None:
        """
        Génère les menus de la moulinette.
        """
        moulinette = MainController.get_moulinette()
        menus = moulinette.menus_tries_par_conflits_et_filtres()

        AppState.update('menus', menus)
        AppState.update('current_menu_index', 0)

    @staticmethod
    def get_menus()->List[_IMenu]:
        """Retourne les menus de la session.

        :return:Les menus
        :rtype: List[_IMenu]
        """
        return AppState.get('menus')

    @staticmethod
    def reset_menus()->None:
        """
        Réinitialise les menus.
        """
        moulinette = MainController.get_moulinette()
        moulinette.reset_menus()

        AppState.update('menus', None)
        AppState.update('current_menu_index', None)
        AppState.update('nb_barrettes', None)
