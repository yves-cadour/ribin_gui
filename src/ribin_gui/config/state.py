import streamlit as st
import pandas as pd
from ribin.moulinette import Moulinette

def init_state():
    """Initialise tous les états nécessaires"""
    if 'etape' not in st.session_state:
        st.session_state.etape = 1
    if 'moulinette' not in st.session_state:
        st.session_state.moulinette = None
    if 'last_upload' not in st.session_state:
        st.session_state.last_upload = None
    if 'seuil_effectif' not in st.session_state:
        st.session_state.seuil_effectif = 25

def handle_upload(uploaded_file):
    """Gère un nouvel upload de fichier"""
    if uploaded_file and st.session_state.last_upload != uploaded_file.name:
        st.session_state.moulinette = Moulinette()
        df = pd.read_csv(uploaded_file)
        st.session_state.moulinette.read_datas(df)
        st.session_state.last_upload = uploaded_file.name
        return True
    return False