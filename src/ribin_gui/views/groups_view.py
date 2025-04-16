import streamlit as st
from ..utils import calculer_separateurs

def render():
    st.title("👥 Gestion des groupes")
    _display_etapes_groupes()

# Étape 2 - Gestion des groupes
def _display_etapes_groupes():

    if not st.session_state.moulinette:
        st.warning("Importez d'abord un fichier valide")
        return

    specialites = st.session_state.moulinette.specialites
    separateurs = calculer_separateurs(len(specialites), 3)
    cols = st.columns(len(separateurs))

    for col, (start, end) in zip(cols, separateurs):
        with col:
            for spe in specialites[start:end]:
                # Récupère le seuil depuis la session
                seuil = st.session_state.get('seuil_effectif', 25)
                with st.expander(f"{spe.icon}{spe.label} ({len(spe.eleves)} élèves)",
                                  expanded=True,
                                  ):
                    # Bouton Ajouter
                    if st.button("➕ Ajouter un groupe", key=f"add_{spe.label}"):
                        st.session_state.moulinette.add_groupe(spe)
                    # Liste des groupes existants
                    if spe.groupes:
                        for groupe in sorted(spe.groupes, key=lambda x: x.number):
                            cols = st.columns([4, 1])
                            # Style conditionnel pour la ligne du groupe
                            effectif = len(groupe.eleves)
                            if effectif >= seuil:
                                cols[0].markdown(f"**🚩🚩 Groupe {groupe.label}: {effectif} élèves 🚩🚩**")
                            else:
                                cols[0].write(f"Groupe {groupe.label}: {effectif} élèves")
                            if groupe.number != 1 and cols[1].button("➖", key=f"del_{groupe.id}"):
                                st.session_state.moulinette.delete_groupe(groupe.id)
                                st.rerun()
                    else:
                        st.warning("Aucun groupe créé")
