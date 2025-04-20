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
    elif menus is None:
        st.info("Générez les menus en cliquant sur le bouton dans la partie gauche.")


def display_menu_navigation():
    """Affiche les boutons de navigation entre menus"""
    menu_index = MenusController.current_menu_index()
    total_menus = len(MainController.get_menus())

    col1, col2, col3 = st.columns([1, 3, 1])

    # Bouton Précédent
    if col1.button("◀ Précédent", disabled=menu_index <= 0):
        MenusController.decremente_menu_index()
        st.rerun()

    # Indicateur de position
    current_menu_index = MenusController.current_menu_index()
    nb_menus = len(MainController.get_menus())
    col2.markdown(f"**Menu {current_menu_index+1} / {nb_menus}**", unsafe_allow_html=True)

    # Bouton Suivant
    if col3.button("Suivant ▶", disabled=menu_index >= total_menus - 1):
        MenusController.incremente_menu_index()
        st.rerun()
def display_menu(menu):
    """
    Affiche les menus générés
    """
    moulinette = MainController.get_moulinette()
    menu_index = MenusController.current_menu_index()
    menus = MainController.get_menus()
    st.subheader(f"Menu {menu_index + 1}/{len(menus)}")

    # Affichage des barrettes
    barrettes = menu.barrettes
    cols = st.columns(len(barrettes), gap="small")

    for i, (col, barrette) in enumerate(zip(cols, barrettes)):
        with col:
            st.markdown(f"**☰&nbsp;&nbsp;BARRETTE {i+1}**")
            for groupe in barrette.groupes:
                spe = groupe.specialite
                st.markdown(f"""
                <div>
                    <b>{spe.icon} {groupe.label}</b><small>&nbsp;{len(groupe.eleves)} élèves</small>
                </div>
                """, unsafe_allow_html=True)

    # Affichage des conflits
    insolubles, potentiels = menu.conflicts(moulinette)
    st.subheader("Conflits par concomitance")
    cols = st.columns(2, gap="small")
    for i, (col, groupes_eleves) in enumerate(zip(cols, (insolubles, potentiels))):
        with col:
            type_conflit = "insolubles" if i == 0 else "potentiels"
            st.markdown(f"**Conflits {type_conflit}**")
            if groupes_eleves:
                for groupes, eleves in groupes_eleves.items():
                    groupes_labels = [f"{g.specialite.icon} {g.label}" for g in groupes]
                    concomitance = ' ⚡ ⚡ ⚡ '.join(groupes_labels)
                    with st.expander(f"Concomitance : {concomitance}", expanded=True):
                        if eleves:
                            st.dataframe(pd.DataFrame(
                                [(f"{e.nom} {e.prenom}", ", ".join(s.label for s in moulinette.get_specialites_for_eleve(e)), ", ".join(g.label for g in moulinette.get_groupes_for_eleve(e)))
                                for e in sorted(eleves, key=moulinette.get_specialites_for_eleve)],
                                columns=["Élève", "Spécialités", "Groupes"]
                            ), hide_index=True)
            else:
                st.info("Aucun conflit")
