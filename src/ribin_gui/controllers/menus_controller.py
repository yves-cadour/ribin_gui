"""Le contrôleur de la vue des menus"""

from typing import Optional

from ribin_gui.state import AppState
from ribin_gui.controllers.main_controller import MainController

class MenusController:
    """
    La classe du contrôleur des menus
    """
    @staticmethod
    def current_menu_index()->Optional[int]:
        """
        Retourne la valeur de l'index du menu courant.

        :return: la valeur de l'index du menu courant
        :rtype: int
        """
        return AppState.get('current_menu_index', int)

    @staticmethod
    def incremente_menu_index()->Optional[int]:
        """Incrémente la valeur de l'index du menu courant.

        :return: la nouvelle valeur de l'index du menu courant.
        :rtype: int
        """
        menus = MainController.get_menus()
        if not menus:
            return None

        current = MenusController.current_menu_index() or 0
        if current < len(menus) - 1:
            new_index = current + 1
            AppState.update('current_menu_index', new_index)
            return new_index
        return current

    @staticmethod
    def decremente_menu_index()->Optional[int]:
        """Décrémente la valeur de l'index du menu courant.

        :return: la nouvelle valeur de l'index du menu courant.
        :rtype: int
        """
        current = MenusController.current_menu_index() or 0
        if current > 0:
            new_index = current - 1
            AppState.update('current_menu_index', new_index)
            return new_index
        return current
