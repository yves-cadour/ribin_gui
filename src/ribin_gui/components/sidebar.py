import streamlit as st
from ribin_gui.config.state import handle_upload, handle_nb_specialites_par_eleve, generate_menus

def sidebar():
    """Composition de la sidebar"""
    with st.sidebar:
        st.title("Navigation")
        display_navigation()

        if st.session_state.etape == 1:
            display_nb_specialites()
            display_upload()
        elif st.session_state.etape == 2:
            display_groups()
        elif st.session_state.etape == 3:
            display_menus()

# +------------------------------------------------------------------------+
# |                       NAVIGATION                                       |
# +------------------------------------------------------------------------+

def display_navigation():
    """Affiche les boutons de navigation"""
    col1, col2 = st.columns(2)
    if st.session_state.etape > 1 and col1.button("← Retour"):
        st.session_state.etape -= 1

    disabled = st.session_state.etape >= 3 or not st.session_state.moulinette
    if col2.button("Suivant →", disabled=disabled):
        st.session_state.etape += 1

# +------------------------------------------------------------------------+
# |               IMPORTATION DES DONNEES                                  |
# +------------------------------------------------------------------------+

def display_nb_specialites():
    """
    Affiche le slider pour le choix du nombre de spécialités par élève.
    """
    disabled = handle_nb_specialites_par_eleve()
    st.session_state.nb_specialites = st.slider(
                "Nombre de spécialités par élève",
                min_value=2,
                max_value=3,
                value=st.session_state.nb_specialites,
                key="slider_nb_specialites",
                disabled=disabled,
            )
    st.info(f"3 spécialités en première, 2 en terminale.")

def display_upload():
    """Affiche le widget d'upload"""
    st.header("1. Données")
    uploaded_file = st.file_uploader("Importer CSV", type=["csv"])
    if uploaded_file and handle_upload(uploaded_file):
        st.success("Fichier importé !")
        st.rerun()

# +------------------------------------------------------------------------+
# |                      GESTION DES GROUPES                               |
# +------------------------------------------------------------------------+

def display_groups():
    """Affiche la gestion des groupes"""
    st.header("2. Groupes")
    st.session_state.seuil_effectif = st.slider(
                "Seuil d'effectif pour mise en évidence",
                min_value=20,
                max_value=30,
                value=st.session_state.seuil_effectif,
                key="slider_effectif"
            )
    st.info(f"Les spécialités ≥ {st.session_state.seuil_effectif} élèves sont mis en évidence.")

# +------------------------------------------------------------------------+
# |                      GESTION DES MENUS                                 |
# +------------------------------------------------------------------------+

def display_menus():
    """Affiche la gestion des menus"""
    moulinette = st.session_state.moulinette
    st.header("3. Menus")
    # Debug visible dans l'UI
    st.caption(f"Valeur actuelle : {st.session_state.get('nb_barrettes')} | Moulinette : {moulinette.nb_barrettes if moulinette else 'N/A'}")

    nb_barrettes = st.slider("Nombre de barrettes",
                            min_value=2,
                            max_value=5,
                            value=moulinette.nb_barrettes,
                            key="nb_barrettes_slider",
                            on_change=cb_update_barrettes)
    st.info(f"{len(moulinette.specialites)} spécialites dans {moulinette.nb_barrettes} barrettes soit {moulinette.nombre_menus_possibles()} menus possibles.")

    max_conflits_certains = st.slider("Maximum de conflits certains",
                                    min_value=1,
                                    max_value=10,
                                    value=moulinette.max_conflits_certains,
                                    key="max_conflits_certains",
                                    on_change=cb_update_max_conflits_certains)

    max_conflits_potentiels_par_conflit_certain = st.slider("Maximum de conflits potentiels par conflit certain",
                                    min_value=1,
                                    max_value=10,
                                    value=moulinette.max_conflits_potentiels_par_conflit_certain,
                                    key="max_conflits_potentiels_par_conflit_certain",
                                    on_change = cb_update_max_conflits_potentiels_par_conflit_certain)
    c = moulinette.max_conflits_certains
    p = moulinette.max_conflits_potentiels_par_conflit_certain
    st.info(f"Il y aura au maximum {c} x {p} = {c*p} meilleurs menus proposés.")

    if st.button("🎯 Générer les menus", type="primary", key="generate_menus"):
       with st.spinner("Génération en cours..."):
            print(f"st.session_state.nb_barrettes : {st.session_state.nb_barrettes}")
            print(f"st.session_state.moulinette.nb_barrettes : {st.session_state.moulinette.nb_barrettes}")
            if not st.session_state.nb_barrettes:
                st.session_state.nb_barrettes = moulinette.nb_barrettes

            try:
                generate_menus()
                st.success("Menus générés avec succès!")
            except ValueError as e:
                st.error(f"Erreur lors de la génération des menus : {e}")

# +------------------------------------------------------------------------+
# |                       CALLBACKS                                        |
# +------------------------------------------------------------------------+

def cb_update_barrettes():
    # Stocke la valeur du slider ET met à jour la moulinette immédiatement
    st.session_state.nb_barrettes = st.session_state.nb_barrettes_slider
    st.session_state.moulinette.nb_barrettes = st.session_state.nb_barrettes  # Synchronisation directe
    st.session_state.menus = None  # Invalide les anciens menus

def cb_update_max_conflits_certains():
    st.session_state.moulinette.max_conflits_certains = st.session_state.max_conflits_certains

def cb_update_max_conflits_potentiels_par_conflit_certain():
    st.session_state.moulinette.max_conflits_potentiels_par_conflit_certain = st.session_state.max_conflits_potentiels_par_conflit_certain



