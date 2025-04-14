import streamlit as st
import pandas as pd  # N'oubliez pas d'importer pandas

def render():
    st.title("Génération des menus")
    _display_menus()

def _display_menus():
    moulinette = st.session_state.moulinette

    if not moulinette:
        st.warning("Complétez les étapes précédentes")
        return

    # Initialisation des variables de session
    if 'menus' not in st.session_state:
        st.session_state.menus = None
    if 'current_menu_index' not in st.session_state:
        st.session_state.current_menu_index = 0

    # Vérification si les menus existent
    if st.session_state.menus:
        menus = st.session_state.menus  # Récupère les menus depuis session_state
        menu_index = st.session_state.current_menu_index

        # Affichage des barrettes
        current_menu = menus[menu_index]
        barrettes = current_menu.barrettes

        # Créer des colonnes pour afficher les barrettes
        cols = st.columns(len(barrettes), gap="small")

        for i, (col, barrette) in enumerate(zip(cols, barrettes)):
            with col:
                st.markdown(f"**☰&nbsp;&nbsp;BARRETTE {i+1}**")
                for groupe in barrette.groupes:
                    spe = groupe.specialite
                    st.markdown(f"""
                    <div style="border-top:1px solid #ccc;padding:5px 0">
                        <b>{spe.icon} {groupe.label}</b><small>&nbsp;{len(groupe.eleves)} élèves</small>
                    </div>
                    """, unsafe_allow_html=True)

        # Affichage des conflits
        certains, potentiels = current_menu.conflicts(moulinette)
        st.subheader("Conflits par concomitance")
        cols = st.columns(2, gap="small")  # Correction: 2 colonnes pour certains/potentiels

        for i, (col, eleves) in enumerate(zip(cols, (certains, potentiels))):
            with col:
                type_conflit = "certains" if i == 0 else "potentiels"
                with st.expander(f"Conflits {type_conflit} ({len(eleves)} élèves)", expanded=True):
                    if eleves:
                        st.dataframe(pd.DataFrame(
                            [(f"{e.nom} {e.prenom}", ", ".join(s.label for s in moulinette.get_specialites_for_eleve(e)))
                            for e in sorted(eleves, key=lambda x: moulinette.get_specialites_for_eleve(x))],
                            columns=["Élève", "Spécialités"]
                        ), hide_index=True)
                    else:
                        st.info("Aucun conflit")

    elif st.session_state.menus is None:
        st.info("Générez les menus en cliquant sur le bouton dans la partie gauche.")