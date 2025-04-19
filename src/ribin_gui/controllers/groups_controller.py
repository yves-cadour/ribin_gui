"""Le contrôleur de la vue des groupes"""

#import streamlit as st
from math import ceil
from typing import Sequence
from ribin.interfaces import _ISpecialite, _IGroupe
from ribin_gui.state import reset_menus
from ribin_gui.controllers import main_controller, sidebar_controller

def get_seuil_effectif()->int:
    """Retourne le seuil effectif pour les groupes.

    :return: le seuil effectif pour les groupes
    :rtype: int
    """
    return sidebar_controller.get_seuil_effectif()

def add_groupe(specialite):
    """Ajoute un groupe à la spécialite
    """
    main_controller.get_moulinette().add_groupe(specialite)
    reset_menus()

def delete_groupe(groupe_id:int):
    """Supprime un groupe

    :param groupe_id: L'id du groupe
    :type groupe_id: int
    """
    main_controller.get_moulinette().delete_groupe(groupe_id)
    reset_menus()

def get_effectif_moyen_par_groupe(specialite:_ISpecialite)->int:
    """Retourne l'effectif moyen par groupe pour une spécialité donnéee.

    :param specialite: la spécialite
    :type specialite: _ISpecialite
    :return: l'effectif moyen
    :rtype: int
    """
    nb_eleves = len(specialite.eleves)
    nb_groups = len(specialite.groupes)
    return ceil(nb_eleves/nb_groups)

def get_groupes_for_specialite(specialite:_ISpecialite)->Sequence[_IGroupe]:
    """Retourne les groupes de la spécialité

    :param specialite: la spécialité
    :type specialite: _ISpecialite
    :return: les groupes de la spécialités triés
    :rtype: Sequence[_IGroupe]
    """
    return sorted(specialite.groupes, key=lambda x: x.number)
