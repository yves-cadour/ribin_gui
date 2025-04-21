"""Le contrôleur de la vue du menu selectionné"""


from typing import Optional
from ribin.interfaces import _IMenu, _IGroupe
from ribin.menu_optimizer import MenuOptimizer
from ribin_gui.state import AppState
from ribin_gui.controllers.menu_controller import MenuOptimizer
from ribin_gui.controllers.menus_controller import MenusController
from ribin_gui.controllers.main_controller import MainController

class MenuController:
    """
    La classe du contrôleur du menu selectionné
    """
    @staticmethod
    def empty_groups()-> list[_IGroupe]:
        moulinette = MainController.get_moulinette()
        menu = MenusController.get_menu()
        optimizer =  MenuOptimizer(moulinette,menu)
        return optimizer.empty_groups