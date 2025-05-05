"""Le contrôleur de la vue des menus"""

from typing import Optional
from ribin.interfaces import _IMenu, _IGroupe
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

    @staticmethod
    def get_menu()->_IMenu:
        """Retourne le menu selectionné.

        :return:Le menu
        :rtype: _IMenu
        """
        #print("menus_controller > get_menu")
        current_menu = AppState.get('menus')[AppState.get('current_menu_index')]
        #print(f"current_menu : {current_menu}")
        return current_menu

    @staticmethod
    def update_menu(new_menu:_IMenu)->bool:
        """
        Met à jour le menu selectionné dans la session.
        Retourne True si il est différent du menu courant, False sinon

        :param new_menu: le menu
        :type new_menu: _IMenu
        :return: True si différent, False sinon.
        :rtype: bool
        """
        menu = MenusController.get_menu()
        if new_menu != menu:
            menus = AppState.get('menus')
            current_menu_index = AppState.get('current_menu_index')
            menus[current_menu_index] = new_menu
            return True
        return False

    @staticmethod
    def deplacer_groupe(groupe:_IGroupe, barrette_number:int)->_IMenu:
        """
        Déplace un groupe dans une barrette

        :param groupe: le groupe à déplacer
        :type groupe: _IGroupe
        :param barrette_number: le numéro de la barrette de destination
        :type barrette_number: int
        :return: le nouveau menu
        :rtype: _IMenu
        """
        print(f"---menus_controller > deplacer_groupe---(groupe:{groupe}, barrette_number:{barrette_number})")
        menu = MenusController.get_menu()
        print(f"menu:{menu}")
        barrette_destination = menu.get_barrette_with_number(barrette_number)
        print(f"barrette_destination : {barrette_destination}")
        menu = menu.with_move_groupe_to_barrette(groupe, barrette_destination)
        print(f"menu:{menu}")
        MenusController.update_menu(menu)
        return menu
