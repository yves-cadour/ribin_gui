"""Une vue pour la résolution des conflits"""

import streamlit as st
import pandas as pd
from ..controllers.main_controller import MainController
from ..controllers.menus_controller import MenusController
from ..views.menus_view import display_menu, display_conflits_insolubles
from ..utils import get_icon, get_label

def render():
    """
    Point d'entrée pour la vue du menu selectionné.
    """
    etape = MainController.get_etape()
    nb_etapes = MainController.get_nb_etapes()
    label, icon = get_label(etape), get_icon(etape)
    st.title(f"{icon} {label} ({etape}/{nb_etapes})")
    selected_menu = MenusController.get_menu()
    if selected_menu is None:
        st.warning("Importez d'abord un fichier valide")
        return
    else:
        display_conflits_insolubles(selected_menu)
        _, potentiels = selected_menu.conflicts(MainController.get_moulinette())
        display_conflits(potentiels)

def display_group_moves():
    """Affiche les suggestions de déplacement de groupes"""
    resolver = st.session_state.current_resolver
    steps = resolver.get_resolution_steps()

    group_moves = [s for s in steps if s['type'] == 'move_group']
    if group_moves:
        st.subheader("Déplacements de groupes recommandés")

        for move in group_moves[:3]:  # Limite à 3 meilleures suggestions
            with st.container(border=True):
                cols = st.columns([3, 1])
                cols[0].markdown(f"**Déplacer {move['group'].label}**")
                cols[0].markdown(f"Vers: {move['targets'][0]['barrette'].label}")
                cols[0].progress(min(100, move['potential_impact'] * 10),
                               text=f"Résoudrait ~{move['potential_impact']} conflits")

                if cols[1].button("Appliquer", key=f"apply_{move['group'].id}"):
                    resolver.apply_group_move(move['group'], move['targets'][0]['barrette'])
                    st.success("Déplacement appliqué!")
                    #st.rerun()

def display_student_moves():
    """Affiche les suggestions de déplacement d'élèves"""
    if 'current_student_moves' not in st.session_state:
        return

    move = st.session_state.current_student_moves
    resolver = st.session_state.current_resolver

    st.subheader(f"Rééquilibrage pour {len(move['students'])} élèves")
    st.write(f"Conflit actuel: {' + '.join(g.label for g in move['conflict'])}")

    solutions = resolver.suggest_student_moves(move['conflict'])
    if solutions:
        st.dataframe(pd.DataFrame(
            [{
                "Élève": f"{s['student'].nom} {s['student'].prenom}",
                "De": s['from_group'].label,
                "Vers": s['to_group'].label,
                "Impact conflit": s['conflict_impact'],
                "Impact équilibre": s['balance_impact']
            } for s in solutions[:10]],  # Limite à 10 meilleures solutions
        ), use_container_width=True)

        if st.button("Appliquer les meilleurs déplacements"):
            apply_student_moves([solutions[0]])  # Applique la meilleure solution
    else:
        st.warning("Aucune solution trouvée pour ce conflit")

def display_group_move_suggestions():
    if 'current_resolver' not in st.session_state:
        return

    resolver = st.session_state.current_resolver
    empty_groups = resolver._find_empty_groups()

    if not empty_groups:
        st.info("Aucun groupe vide disponible pour déplacement")
        return

    st.subheader("Groupes vides déplaçables")
    for group in empty_groups:
        with st.expander(f"{group.label} (Spé: {group.specialite.label})"):
            targets = resolver._find_best_barrettes_for_group(group)

            if not targets:
                st.warning("Aucune barrette cible optimale trouvée")
                continue

            best_target = targets[0]
            cols = st.columns([3, 1])
            cols[0].markdown(f"""
                **Meilleure cible:**
                {best_target['barrette'].label}
                Conflits résolus: {best_target['conflicts_resolved']}
                Amélioration équilibre: {best_target['balance_impact']:.2f}
            """)

            if cols[1].button("Déplacer", key=f"move_{group.id}"):
                resolver.apply_group_move(group, best_target['barrette'])
                st.success(f"Groupe {group.label} déplacé !")
                #st.rerun()

            # Afficher d'autres options
            st.markdown("**Autres options valides:**")
            for target in targets[1:3]:  # Affiche les 2 suivantes
                st.markdown(f"""
                    - {target['barrette'].label}
                    (Score: {target['score']:.2f},
                    Conflits: {target['conflicts_resolved']})
                """)