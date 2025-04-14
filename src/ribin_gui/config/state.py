
import streamlit as st

# Initialisation de l'état
def init_state():
    if 'etape' not in st.session_state:
        st.session_state.etape = 1  # 1=Import, 2=Groupes, 3=Menus
    if 'moulinette' not in st.session_state:
        st.session_state.moulinette = None


def reset_application_state():
    """Réinitialise complètement l'état de l'application"""
    st.session_state.moulinette = None
    st.session_state.menus = None
    st.session_state.current_menu_index = 0
    st.session_state.etape = 1  # Retour à l'étape 1

def reset_menus(origine = ""):
    debug = True
    if debug:
        print(f"reset_menus from {origine}")
    if 'menus' in st.session_state:
        if debug:
            print("RESET MENUS")
        st.session_state.menus = None
        #st.rerun()
    else:
        if debug:
            print("'menus' not in st.session_state")

def handle_upload_complete():
    """Gère la complétion d'un upload de manière atomique"""
    if st.session_state.get('upload_in_progress', False):
        st.session_state.upload_in_progress = False
        st.session_state.file_just_uploaded = True
    else:
        st.session_state.file_just_uploaded = False