"""La vue de la barre latérale"""

import streamlit as st
from ..controllers.main_controller import MainController
from ..controllers.sidebar_controller import SidebarController


def render():
    """Composition de la sidebar"""
    with st.sidebar:
        sidebar_navigation()
        etape = MainController.get_etape()
        if etape == 1:
            sidebar_nb_specialites()
            sidebar_upload()
        elif etape == 2:
            sidebar_groups()
        elif etape == 3:
            sidebar_menus()
        # elif etape == 4:  # Nouvelle étape
        #     side_conflict_resolution()

# +------------------------------------------------------------------------+
# |                       NAVIGATION                                       |
# +------------------------------------------------------------------------+

def sidebar_navigation():
    """Affiche les boutons de navigation"""
    etape = MainController.get_etape()
    nb_etapes = MainController.get_nb_etapes()
    moulinette = MainController.get_moulinette()
    st.title("Navigation")
    col1, col2 = st.columns(2)
    if etape > 1 and col1.button("← Retour",
                                 key='previous',
                                 type='primary'):
        MainController.decrementer_etape()
        st.rerun()
    if etape < nb_etapes and col2.button("Suivant →",
                   key="next",
                   type='primary',):
        if moulinette is None:
            st.error("Veuillez d'abord uploader un fichier valide.")
        else:
            MainController.incrementer_etape()
            st.rerun()

# +------------------------------------------------------------------------+
# |               IMPORTATION DES DONNEES                                  |
# +------------------------------------------------------------------------+

def sidebar_nb_specialites():
    """
    Affiche le slider pour le choix du nombre de spécialités par élève.
    """
    etape = MainController.get_etape()
    st.header(f"{etape}. Données")
    nb_specialites = st.slider(
                "Nombre de spécialités par élève",
                min_value=2,
                max_value=3,
                help="3 spécialités en première, 2 en terminale.",
                key="nb_specialites",
            )
    if nb_specialites:
        if SidebarController.update_nb_specialites(nb_specialites):
            st.info('Moulinette réinitialisée')

def sidebar_upload():
    """Affiche le widget d'upload"""
    uploaded_file = st.file_uploader("Importer CSV",
                                     type=["csv"],
                                     key ="file_uploader")
    if uploaded_file:
        if SidebarController.handle_upload(uploaded_file):
            st.success("Fichier importé avec succès !")


# +------------------------------------------------------------------------+
# |                      GESTION DES GROUPES                               |
# +------------------------------------------------------------------------+

def sidebar_groups():
    """Affiche la gestion des groupes"""
    etape = MainController.get_etape()
    st.header(f"{etape}. Groupes")
    # 1. Récupérer la valeur actuelle UNE FOIS
    current_seuil = SidebarController.get_seuil_effectif()

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
        SidebarController.update_seuil_effectif(new_seuil)
        st.rerun()  # Force une actualisation propre

    # 4. Afficher la valeur actuelle
    st.info(f"Les spécialités ≥ {current_seuil} élèves sont mis en évidence.")

# +------------------------------------------------------------------------+
# |                      GESTION DES MENUS                                 |
# +------------------------------------------------------------------------+

def sidebar_menus():
    """Affiche la gestion des menus"""
    moulinette = MainController.get_moulinette()
    etape = MainController.get_etape()
    st.header(f"{etape}. Menus")

    help_widget = f"{len(MainController.get_moulinette().specialites)} spécialites \
            dans {MainController.get_moulinette().nb_barrettes} barrettes \
            soit {MainController.get_moulinette().nombre_menus_possibles()} menus."

    # nb_barrettes
    nb_barrettes = st.slider("Nombre de barrettes",
                            min_value=2,
                            max_value=5,
                            value=moulinette.nb_barrettes,
                            help = help_widget,
                            key="nb_barrettes_widget",)
    if nb_barrettes!=moulinette.nb_barrettes:
        if SidebarController.update_nb_barrettes(nb_barrettes):
            st.rerun()
    col1, col2 = st.columns(2)
    with col1:
        # max_conflits_certains
        max_conflits = st.slider("Maximum de conflits insolubles",
                    min_value=1,
                    max_value=10,
                    value=moulinette.max_conflits_certains,
                    key="max_conflits_certains",)
        if max_conflits!=moulinette.max_conflits_certains:
            SidebarController.update_max_conflits(max_conflits, conflict_type='insolubles')
            st.rerun()
    with col2:
        # max_conflits_potentiels_par_conflit_certain
        max_potentiels = st.slider("Maximum de conflits potentiels par conflit insoluble",
                    min_value=1,
                    max_value=10,
                    value=moulinette.max_conflits_potentiels_par_conflit_certain,
                    key="max_conflits_potentiels_par_conflit_certain",)
        if max_potentiels!=moulinette.max_conflits_potentiels_par_conflit_certain:
            SidebarController.update_max_conflits(max_potentiels, conflict_type='potentiels')
            st.rerun()
    c = moulinette.max_conflits_certains
    p = moulinette.max_conflits_potentiels_par_conflit_certain
    st.info(f"Il y aura au maximum {c} x {p} = {c*p} meilleurs menus proposés.")

    if st.button("⚙️ Générer les menus", type="primary", key="generate_menus"):
        with st.spinner("Génération en cours..."):
            MainController.generer_menus()
            st.success(f"{len(MainController.get_menus())} meilleurs menus générés avec succès!")

# +------------------------------------------------------------------------+
# |                       RESOLUTION DES CONFLITS                          |
# +------------------------------------------------------------------------+
# def side_conflict_resolution():
#     """Affiche les contrôles pour la résolution des conflits"""
#     st.header("4. Résolution des conflits")

#     if st.button("🔍 Analyser les conflits", key="analyze_conflicts"):
#         #st.session_state.current_resolver =
#         #st.rerun()
#         pass

#     if 'current_resolver' in st.session_state:
#         st.subheader("Actions recommandées")
#         steps = st.session_state.current_resolver.get_resolution_steps()

#         for step in steps[:3]:  # Affiche les 3 meilleures suggestions
#             if step['type'] == 'move_group':
#                 with st.expander(f"📦 Déplacer groupe {step['group'].label}"):
#                     st.write(f"Vers barrette: {step['targets'][0]['barrette'].label}")
#                     st.write(f"Résoudrait {step['potential_impact']} conflits")
#                     if st.button("Appliquer", key=f"move_group_{step['group'].id}"):
#                         apply_group_move(step['group'], step['targets'][0]['barrette'])

#             elif step['type'] == 'move_students':
#                 with st.expander(f"👥 Rééquilibrer {len(step['students'])} élèves"):
#                     st.write(f"Conflit: {', '.join(g.label for g in step['conflict'])}")
#                     st.dataframe(pd.DataFrame(
#                         [(s.nom, s.prenom) for s in step['students']],
#                         columns=["Nom", "Prénom"]
#                     ))
#                     if st.button("Afficher solutions", key=f"show_solutions_{hash(step['conflict'])}"):
#                         st.session_state.current_student_moves = step
#                         #st.rerun()
