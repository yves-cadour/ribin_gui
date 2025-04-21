"""Une vue pour les menus"""


import streamlit as st
import pandas as pd

from ..controllers.main_controller import MainController
from ..controllers.menus_controller import MenusController
from ..utils import get_icon, get_label

def render():
    """
    Point d'entrée pour la vue des menus générés
    """
    etape = MainController.get_etape()
    nb_etapes = MainController.get_nb_etapes()
    label, icon = get_label(etape), get_icon(etape)
    st.title(f"{icon} {label} ({etape}/{nb_etapes})")

    # Ajout des boutons de navigation entre menus
    menus = MainController.get_menus()
    if menus:
        display_menu_navigation()
        current_menu = menus[MenusController.current_menu_index()]
        display_menu(current_menu)
        # Affichage des conflits
        current_menu = menus[MenusController.current_menu_index()]
        insolubles, potentiels = current_menu.conflicts(MainController.get_moulinette())
        st.subheader("Conflits par concomitance")
        col1, col2 = st.columns(2, gap="small")
        with col1:
            display_conflits(insolubles, title="Conflits insolubles")
        with col2:
            display_conflits(potentiels, title="Conflits potentiels")
    elif menus is None:
        st.info("Générez les menus en cliquant sur le bouton dans la partie gauche.")


def display_menu_navigation():
    """Affiche les boutons de navigation entre menus"""
    menus = MainController.get_menus()
    menu_index = MenusController.current_menu_index()
    current_menu = menus[MenusController.current_menu_index()]
    nb_menus = len(MainController.get_menus())

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    # Bouton Précédent
    if col1.button("◀ Précédent", disabled=menu_index <= 0):
        MenusController.decremente_menu_index()
        st.rerun()

    # Indicateur de position
    current_menu_index = MenusController.current_menu_index()
    col2.subheader(f"📋 Menu {current_menu_index+1} / {nb_menus}")

    # Selection du menu courant
    if col4.button("Choisir ce menu",
                   key="menu_selection",
                   type = 'primary',
                   icon='👆'):
        MenusController.update_menu(current_menu)
        MainController.incrementer_etape()
        st.rerun()

    # Bouton Suivant
    if col3.button("Suivant ▶"):
        MenusController.incremente_menu_index()
        st.rerun()

def display_menu(menu):
    """
    Affiche les menus générés
    """
    menu_index = MenusController.current_menu_index()
    menus = MainController.get_menus()
    st.subheader(f"Menu {menu_index + 1}/{len(menus)}")

    # Affichage des barrettes
    barrettes = menu.barrettes
    cols = st.columns(len(barrettes), gap="small")

    for i, (col, barrette) in enumerate(zip(cols, barrettes)):
        with col:
            st.markdown(f"**☰&nbsp;&nbsp;BARRETTE {barrette.number}**")
            for groupe in barrette.groupes:
                spe = groupe.specialite
                st.markdown(f"""
                <div>
                    <b>{spe.icon} {groupe.label}</b><small>&nbsp;{len(groupe.eleves)} élèves</small>
                </div>
                """, unsafe_allow_html=True)

def display_conflits(groupes_eleves, title = "conflits"):
    moulinette = MainController.get_moulinette()
    current_menu = MainController.get_menus()[MenusController.current_menu_index()]
    st.markdown(f"{title}")
    if groupes_eleves:
        for groupes, eleves in groupes_eleves.items():
            concomitances = current_menu.get_concomitances_for_groupes(groupes)
            concomitances_textes = []
            for groupes_conflits, barrette_concernee in concomitances.items():
                concomitances_textes.append((f"{' ⚡ '.join([''.join([g.specialite.icon, g.label]) for g in groupes_conflits])} sur BARRETTE {barrette_concernee.number}"))
            with st.expander(f"Concomitance : {'/ '.join(concomitances_textes)}", expanded=True):
                if eleves:
                    st.dataframe(pd.DataFrame(
                        [(f"{e.nom} {e.prenom}", ", ".join(g.label for g in moulinette.get_groupes_for_eleve(e)))
                        for e in sorted(eleves, key=moulinette.get_specialites_for_eleve)],
                        columns=["Élève", "Groupes"]),
                        hide_index=True,
)
    else:
        st.info("Aucun conflit")