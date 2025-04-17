import streamlit as st
from ribin.moulinette import Moulinette
import pandas as pd

def handle_upload(uploaded_file):
    """Gère un nouvel upload de fichier"""
#    if uploaded_file and st.session_state.last_upload != uploaded_file.name:
    if uploaded_file:
        try:
            # Initialisation de la moulinette (Modèle)
            st.session_state.moulinette = Moulinette()
            st.session_state.nb_specialites = st.session_state.moulinette.nb_specialites

            # Lecture des données
            df = pd.read_csv(uploaded_file)
            st.session_state.moulinette.read_datas(df)

            # Mise à jour de l'état
            #st.session_state.last_upload = uploaded_file.name
            st.session_state.etape = 1  # Ou l'étape appropriée pour afficher datas_view

            return True
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier: {e}")
            return False
    return False