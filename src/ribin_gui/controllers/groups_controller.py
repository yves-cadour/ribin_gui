"""Le contrôleur de la vue des groupes"""

from math import ceil
from typing import Sequence
from ribin.interfaces import _ISpecialite, _IGroupe
from ribin_gui.state import AppState
from ribin_gui.controllers.main_controller import MainController


class GroupsController:
    """
    Un contrôleur pour les groupes
    """

    @staticmethod
    def get_seuil_effectif()->int:
        """
        Retourne le seuil effectif pour les groupes.

        :return: le seuil effectif pour les groupes.
        :rtype: int
        """
        return AppState.get('seuil_effectif', int)

    @staticmethod
    def add_groupe(specialite)->None:
        """
        Ajoute un groupe à la spécialite.
        """
        moulinette = MainController.get_moulinette()
        moulinette.add_groupe(specialite)
        MainController.reset_menus()

    @staticmethod
    def delete_groupe(groupe_id:int)->None:
        """
        Supprime un groupe.

        :param groupe_id: L'id du groupe.
        :type groupe_id: int
        """
        moulinette = MainController.get_moulinette()
        moulinette.delete_groupe(groupe_id)
        MainController.reset_menus()


    @staticmethod
    def get_effectif_moyen_par_groupe(specialite:_ISpecialite)->int:
        """
        Retourne l'effectif moyen par groupe pour une spécialité donnéee.

        :param specialite: la spécialite
        :type specialite: _ISpecialite
        :return: l'effectif moyen
        :rtype: int
        """
        nb_eleves = len(specialite.eleves)
        nb_groups = len(specialite.groupes)
        return ceil(nb_eleves / nb_groups) if nb_groups > 0 else 0

    @staticmethod
    def get_groupes_for_specialite(specialite:_ISpecialite)->Sequence[_IGroupe]:
        """
        Retourne les groupes de la spécialité.

        :param specialite: la spécialité
        :type specialite: _ISpecialite
        :return: les groupes de la spécialités triés
        :rtype: Sequence[_IGroupe]
        """
        return sorted(specialite.groupes, key=lambda x: x.number)
