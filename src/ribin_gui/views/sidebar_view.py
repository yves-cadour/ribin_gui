"""La vue de la barre latérale"""

import streamlit as st
from ..controllers import sidebar_controller


def render():
    """Composition de la sidebar"""
    with st.sidebar:
        sidebar_navigation()
        if st.session_state.etape == 1:
            sidebar_nb_specialites()
            sidebar_upload()
        elif st.session_state.etape == 2:
            sidebar_groups()
        elif st.session_state.etape == 3:
            sidebar_menus()
        elif st.session_state.etape == 4:  # Nouvelle étape
            side_conflict_resolution()

# +------------------------------------------------------------------------+
# |                       NAVIGATION                                       |
# +------------------------------------------------------------------------+

def sidebar_navigation():
    """Affiche les boutons de navigation"""
    st.title("Navigation")
    col1, col2 = st.columns(2)
    if st.session_state.etape > 1 and col1.button("← Retour"):
        st.session_state.etape -= 1
    if col2.button("Suivant →"):
        if st.session_state.moulinette is None:
            st.error("Veuillez d'abord uploader un fichier valide")
        else:
            st.session_state.etape += 1

# +------------------------------------------------------------------------+
# |               IMPORTATION DES DONNEES                                  |
# +------------------------------------------------------------------------+

def sidebar_nb_specialites():
    """
    Affiche le slider pour le choix du nombre de spécialités par élève.
    """
    nb_specialites = st.slider(
                "Nombre de spécialités par élève",
                min_value=2,
                max_value=3,
                key="nb_specialites",
            )
    st.info("3 spécialités en première, 2 en terminale.")
    if nb_specialites:
        if sidebar_controller.update_nb_specialites(nb_specialites):
            st.info('Moulinette réinitialisée')

def sidebar_upload():
    """Affiche le widget d'upload"""
    st.header("1. Données")
    uploaded_file = st.file_uploader("Importer CSV",
                                     type=["csv"],
                                     key ="file_uploader")
    if uploaded_file:
        if sidebar_controller.handle_upload(uploaded_file):
            st.success("Fichier importé avec succès !")


# +------------------------------------------------------------------------+
# |                      GESTION DES GROUPES                               |
# +------------------------------------------------------------------------+

def sidebar_groups():
    """Affiche la gestion des groupes"""
    st.header("2. Groupes")
    # 1. Récupérer la valeur actuelle UNE FOIS
    current_seuil = sidebar_controller.get_seuil_effectif()

    # 2. Afficher le slider avec cette valeur
    new_seuil = st.slider(
        "Seuil d'effectif",
        min_value=20,
        max_value=30,
        value=current_seuil,  # Utilise la valeur pré-chargée
        key="seuil_effectif_widget"
    )
    # 3. Mettre à jour seulement si changement !!!
    if new_seuil != current_seuil:
        sidebar_controller.update_seuil_effectif(new_seuil)
        st.rerun()  # Force une actualisation propre

    # 4. Afficher la valeur actuelle
    st.info(f"Les spécialités ≥ {sidebar_controller.get_seuil_effectif()} élèves sont mis en évidence.")

# +------------------------------------------------------------------------+
# |                      GESTION DES MENUS                                 |
# +------------------------------------------------------------------------+

def sidebar_menus():
    """Affiche la gestion des menus"""


    moulinette = st.session_state.moulinette
    st.header("3. Menus")
    # Debug visible dans l'UI
    #st.caption(f"Valeur actuelle : {st.session_state.get('nb_barrettes')} | Moulinette : {moulinette.nb_barrettes if moulinette else 'N/A'}")

    # nb_barrettes
    nb_barrettes = st.slider("Nombre de barrettes",
                            min_value=2,
                            max_value=5,
                            value=moulinette.nb_barrettes,
                            key="nb_barrettes_slider",)
    if nb_barrettes:
        result_nb_barrettes = update_nb_barrettes(nb_barrettes)
        st.info(f"{len(moulinette.specialites)} spécialites dans {moulinette.nb_barrettes} barrettes soit {moulinette.nombre_menus_possibles()} menus.")
    col1, col2 = st.columns(2)
    with col1:
        # max_conflits_certains
        max_conflits = st.slider("Maximum de conflits certains",
                    min_value=1,
                    max_value=10,
                    value=moulinette.max_conflits_certains,
                    key="max_conflits_certains",)
        if max_conflits:
            result_max_conflits = update_max_conflits_certains(max_conflits)
    with col2:
        # max_conflits_potentiels_par_conflit_certain
        max_potentiels = st.slider("Maximum de conflits potentiels par conflit certain",
                    min_value=1,
                    max_value=10,
                    value=moulinette.max_conflits_potentiels_par_conflit_certain,
                    key="max_conflits_potentiels_par_conflit_certain",)
        if max_potentiels:
            result_max_potentiels = update_max_conflits_potentiels(max_potentiels)
    #c = moulinette.max_conflits_certains
    #p = moulinette.max_conflits_potentiels_par_conflit_certain
    #st.info(f"Il y aura au maximum {c} x {p} = {c*p} meilleurs menus proposés.")

    if st.button("🎯 Générer les menus", type="primary", key="generate_menus"):
       with st.spinner("Génération en cours..."):
            if not st.session_state.nb_barrettes:
                st.session_state.nb_barrettes = moulinette.nb_barrettes

            try:
                generate_menus()
                st.success("Menus générés avec succès!")
            except ValueError as e:
                st.error(f"Erreur lors de la génération des menus : {e}")

# +------------------------------------------------------------------------+
# |                       RESOLUTION DES CONFLITS                          |
# +------------------------------------------------------------------------+
def side_conflict_resolution():
    """Affiche les contrôles pour la résolution des conflits"""
    st.header("4. Résolution des conflits")

    if st.button("🔍 Analyser les conflits", key="analyze_conflicts"):
        #st.session_state.current_resolver =
        #st.rerun()
        pass

    if 'current_resolver' in st.session_state:
        st.subheader("Actions recommandées")
        steps = st.session_state.current_resolver.get_resolution_steps()

        for step in steps[:3]:  # Affiche les 3 meilleures suggestions
            if step['type'] == 'move_group':
                with st.expander(f"📦 Déplacer groupe {step['group'].label}"):
                    st.write(f"Vers barrette: {step['targets'][0]['barrette'].label}")
                    st.write(f"Résoudrait {step['potential_impact']} conflits")
                    if st.button("Appliquer", key=f"move_group_{step['group'].id}"):
                        apply_group_move(step['group'], step['targets'][0]['barrette'])

            elif step['type'] == 'move_students':
                with st.expander(f"👥 Rééquilibrer {len(step['students'])} élèves"):
                    st.write(f"Conflit: {', '.join(g.label for g in step['conflict'])}")
                    st.dataframe(pd.DataFrame(
                        [(s.nom, s.prenom) for s in step['students']],
                        columns=["Nom", "Prénom"]
                    ))
                    if st.button("Afficher solutions", key=f"show_solutions_{hash(step['conflict'])}"):
                        st.session_state.current_student_moves = step
                        #st.rerun()

# +------------------------------------------------------------------------+
# |                       CALLBACKS                                        |
# +------------------------------------------------------------------------+

# def cb_update_barrettes():
#     # Stocke la valeur du slider ET met à jour la moulinette immédiatement
#     print("cb_update_barrettes")
#     st.session_state.nb_barrettes = st.session_state.nb_barrettes_slider
#     st.session_state.moulinette.nb_barrettes = st.session_state.nb_barrettes  # Synchronisation directe
#     delete_menus() # Suppression des menus générés

# def cb_update_max_conflits_certains():
#     print("cb_update_max_conflits_certains")
#     st.session_state.moulinette.max_conflits_certains = st.session_state.max_conflits_certains
#     delete_menus() # Suppression des menus générés

# def cb_update_max_conflits_potentiels_par_conflit_certain():
#     print("cb_update_max_conflits_potentiels_par_conflit_certain")
#     st.session_state.moulinette.max_conflits_potentiels_par_conflit_certain = st.session_state.max_conflits_potentiels_par_conflit_certain
#     delete_menus() # Suppression des menus générés



