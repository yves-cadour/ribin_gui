"""Une vue pour les menus"""


import streamlit as st
import pandas as pd

def display_menu_navigation():
    """Affiche les boutons de navigation entre menus"""
    menu_index = st.session_state.current_menu_index
    total_menus = len(st.session_state.menus)

    col1, col2, col3 = st.columns([1, 3, 1])

    # Bouton Précédent
    if col1.button("◀ Précédent", disabled=(menu_index <= 0)):
        if menu_index > 0:
            st.session_state.current_menu_index -= 1
            st.rerun()

    # Indicateur de position
    col2.markdown(f"**Menu {menu_index + 1} / {total_menus}**", unsafe_allow_html=True)

    # Bouton Suivant
    if col3.button("Suivant ▶", disabled=(menu_index >= total_menus - 1)):
        if menu_index < total_menus - 1:
            st.session_state.current_menu_index += 1
            st.rerun()
def render():
    st.title("Génération des menus")

    # Ajout des boutons de navigation entre menus
    if st.session_state.get('menus'):
        display_menu_navigation()

    moulinette = st.session_state.moulinette

    if st.session_state.menus:
        menus = st.session_state.menus
        menu_index = st.session_state.current_menu_index
        current_menu = menus[menu_index]
        # Affichage du numéro du menu actuel
        st.subheader(f"Menu {menu_index + 1}/{len(menus)}")

        # Affichage des barrettes
        barrettes = current_menu.barrettes
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
        insolubles, potentiels = current_menu.conflicts(moulinette)
        st.subheader("Conflits par concomitance")
        cols = st.columns(2, gap="small")
        for i, (col, set_groupes_eleves) in enumerate(zip(cols, (insolubles, potentiels))):
            with col:
                type_conflit = "insolubles" if i == 0 else "potentiels"
                st.markdown(f"**Conflits {type_conflit}**")
                if set_groupes_eleves:
                    for groupes, eleves in set_groupes_eleves.items():
                        groupes_labels = [f"{g.specialite.icon} {g.label}" for g in groupes]
                        with st.expander(f"Concomitance : {' ⚡ ⚡ ⚡ '.join(groupes_labels)}", expanded=True):
                            if eleves:
                                st.dataframe(pd.DataFrame(
                                    [(f"{e.nom} {e.prenom}", ", ".join(s.label for s in moulinette.get_specialites_for_eleve(e)), ", ".join(g.label for g in moulinette.get_groupes_for_eleve(e)))
                                    for e in sorted(eleves, key=moulinette.get_specialites_for_eleve)],
                                    columns=["Élève", "Spécialités", "Groupes"]
                                ), hide_index=True)
                else:
                    st.info("Aucun conflit")

    elif st.session_state.menus is None:
        st.info("Générez les menus en cliquant sur le bouton dans la partie gauche.")

