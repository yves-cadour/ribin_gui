import streamlit as st


def render():
    st.title("Génération des menus")
    _display_menus()

# Étape 3 - Génération des menus
def _display_menus():
    moulinette = st.session_state.moulinette

    if not moulinette:
        st.warning("Complétez les étapes précédentes")
        return
    if 'menus' not in st.session_state:
        st.session_state.menus = None
    if 'current_menu_index' not in st.session_state:
        st.session_state.current_menu_index = 0


        # Affichage des barrettes
        current_menu = menus[menu_index]
        barrettes = current_menu.barrettes  # C'est un FrozenSet[Barrette]

        # Créer des colonnes pour afficher les barrettes
        cols = st.columns(len(barrettes), gap="small")

        for i, (col, barrette) in enumerate(zip(cols, barrettes)):
            with col:
                st.markdown(f"**☰&nbsp;&nbsp;BARRETTE {i+1}**")
                # Afficher les groupes de la barrette
                for groupe in barrette.groupes:  # Utilisez la propriété groupes
                    spe = groupe.specialite
                    st.markdown(f"""
                    <div style="border-top:1px solid #ccc;padding:5px 0">
                        <b>{spe.icon} {groupe.label}</b><small>&nbsp;{len(groupe.eleves)} élèves</small>
                    </div>
                    """, unsafe_allow_html=True)

        # Affichage des conflits
        certains, potentiels = current_menu.conflicts(moulinette)
        st.subheader("Conflits par concomitance")
        cols = st.columns(len((certains, potentiels)), gap="small")
        for i, (col, eleves) in enumerate(zip(cols, (certains, potentiels))):
            with col:
                with st.expander(f"Conflits {"certains" if i==0 else "potentiels" } ({len(eleves)} élèves)", expanded=True):
                    if eleves:
                        st.dataframe(pd.DataFrame(
                            [(f"{e.nom} {e.prenom}", ", ".join(s.label for s in moulinette.get_specialites_for_eleve(e)))
                            for e in sorted(eleves, key=lambda x: moulinette.get_specialites_for_eleve(x))],
                            columns=["Élève", "Spécialités"]
                        ), hide_index=True)
                        # for eleve in certains:
                        #     conflits_eleve = st.session_state.moulinette.get_conflicts_for_eleve_in_menu(eleve, st.session_state.menus[0])
                        #     for barrette, groupes in conflits_eleve:
                        #         st.markdown(f"**Conflits dans la barrette {barrette.label}**")
                        #         for groupe in groupes:
                        #             st.markdown(f"- {groupe.specialite.label} ({groupe.label})")
                    else:
                        st.info("Aucun conflit")

    elif 'menus' in st.session_state and st.session_state.menus is None:
        st.info("Générez les menus en cliquant sur le bouton dans la partie gauche.")
