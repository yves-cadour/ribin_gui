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
        col1, col2 = st.columns(2, gap='small')
        with col1:
            # Affichage des conflits
            current_menu = menus[MenusController.current_menu_index()]
            insolubles, potentiels = current_menu.conflicts(MainController.get_moulinette())
            st.subheader("Conflits par concomitance")
            tab1, tab2 = st.tabs(["Conflits insolubles", "Conflits potentiels"])
            with tab1:
                display_conflits(insolubles)
            with tab2:
                display_conflits(potentiels)
        with col2:
            st.subheader("Transferts possibles")
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
    print(menu)
    # Affichage des barrettes
    barrettes = menu.barrettes
    cols = st.columns(len(barrettes), gap="small", border=True)

    for (col, barrette) in zip(cols, barrettes):
        with col:
            st.markdown(f"**☰&nbsp;&nbsp;BARRETTE {barrette.number}**")
            for groupe in sorted(barrette.groupes, key=lambda g:g.label):
                if groupe.is_default:
                    spe = groupe.specialite
                    col1, col2, col3 = st.columns([1, 4, 1])
                    with col2:
                        st.markdown(f"""
                        <div>
                            <b>{spe.icon} {groupe.label}</b><small>&nbsp;{len(groupe.eleves)} élèves</small>
                        </div>
                        """, unsafe_allow_html=True)
    cols = st.columns(len(barrettes), gap="small", border=False)
    for (col, barrette) in zip(cols, barrettes):
        with col:
            for groupe in sorted(barrette.groupes, key=lambda g:g.label):
                barrette_number =barrette.number
                if not groupe.is_default:
                    spe = groupe.specialite
                    col1, col2, col3 = st.columns([1, 4, 1])
                    with col1:
                        barrette_precedente_number = (barrette_number-1)%len(barrettes)
                        if st.button("◀", key=f"previous_barrette_for_{groupe.label}", help=f"Déplacer dans la barrette {barrette_precedente_number}."):
                            MenusController.deplacer_groupe(groupe, barrette_number = barrette_precedente_number)
                            st.rerun()

                    with col3:
                        barrette_suivante_number = (barrette_number+1)%len(barrettes)
                        if st.button("▶", key=f"next_barrette_for_{groupe.label}", help=f"Déplacer dans la barrette {barrette_suivante_number}."):
                            MenusController.deplacer_groupe(groupe, barrette_number = barrette_suivante_number)
                            st.rerun()
                    with col2:
                        st.markdown(f"""
                        <div>
                            <b>{spe.icon} {groupe.label}</b><small>&nbsp;{len(groupe.eleves)} élèves</small>
                        </div>
                        """, unsafe_allow_html=True)



def display_conflits(groupes_eleves):
    moulinette = MainController.get_moulinette()
    current_menu = MainController.get_menus()[MenusController.current_menu_index()]
    if not groupes_eleves:
        st.info("Aucun conflit détecté")
        return
    for groupes, eleves in groupes_eleves.items():
        # 1. Construction du texte de concomitance
        concomitances = current_menu.get_concomitances_for_groupes(groupes)
        conflit_texts = []
        for groupes_conflits, barrette in concomitances.items():
            groupes_labels = [
                f"{g.specialite.icon} {g.label}"
                for g in groupes_conflits
            ]
            conflit_texts.append(
                f"{' ⚡ '.join(groupes_labels)} (Barrette {barrette.number})"
            )
        # 2. Affichage dans un expander
        expander_label = f"Concomitance : {' / '.join(conflit_texts)}"
        with st.expander(expander_label, expanded=True):
            if not eleves:
                st.warning("Aucun élève concerné")
                continue
            # 3. Préparation des données pour le DataFrame
            eleves_data = []
            for eleve in sorted(eleves, key=lambda e: (e.nom, e.prenom)):
                groupes_eleve = moulinette.get_groupes_for_eleve(eleve)
                eleves_data.append({
                    "Élève": f"{eleve.nom} {eleve.prenom}",
                    "Groupes": ", ".join(g.label for g in groupes_eleve)
                })
            # 4. Affichage du tableau
            st.dataframe(
                pd.DataFrame(eleves_data),
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Élève": st.column_config.TextColumn(width="medium"),
                    "Groupes": st.column_config.TextColumn(width="large")
                }
            )
