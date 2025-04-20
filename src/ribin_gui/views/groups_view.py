"""La vue des groupes"""

import streamlit as st

from ..controllers.main_controller import MainController
from ..controllers.groups_controller import GroupsController
from ..utils import calculer_separateurs, get_icon, get_label

def render():
    """
    Entrée principale de la vue
    """
    etape = MainController.get_etape()
    nb_etapes = MainController.get_nb_etapes()
    label, icon = get_label(etape), get_icon(etape)
    st.title(f"{icon} {label} ({etape}/{nb_etapes})")

    # récupération des variables
    moulinette = MainController.get_moulinette()
    if not moulinette:
        st.warning("Importez d'abord un fichier valide")
        return
    specialites = moulinette.specialites
    separateurs = calculer_separateurs(len(specialites), 5)
    seuil = GroupsController.get_seuil_effectif()

    cols = st.columns(len(separateurs))
    for col, (start, end) in zip(cols, separateurs):
        with col:
            for spe in specialites[start:end]:
                effectif_moyen = GroupsController.get_effectif_moyen_par_groupe(spe)
                with st.expander(f"**{spe.label}** ({len(spe.eleves)} élèves)",
                                  expanded=True,
                                  icon=spe.icon,
                                  ):
                    # Bouton Ajouter
                    button_type = 'primary' if effectif_moyen>=seuil else 'secondary'
                    if st.button("➕ Ajouter un groupe",
                                 type=button_type,
                                  key=f"add_{spe.label}"):
                        GroupsController.add_groupe(spe)
                        st.rerun()
                    # Liste des groupes existants
                    if spe.groupes:
                        g_for_spe = GroupsController.get_groupes_for_specialite(spe)
                        for i, groupe in enumerate(g_for_spe):
                            cols = st.columns([4, 1])
                            # Style conditionnel pour la ligne du groupe
                            effectif = len(groupe.eleves)
                            cols[0].write(f"Groupe **{groupe.label}**: {effectif} élèves")
                            if i != 0 and cols[1].button("➖", key=f"del_{groupe.id}"):
                                GroupsController.delete_groupe(groupe.id)
                                st.rerun()
                    else:
                        st.warning("Aucun groupe créé")
