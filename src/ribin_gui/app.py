import streamlit as st
from ribin_gui.config.session import init_session
from ribin_gui.views import datas_view, groups_view, menus_view
from ribin_gui.components import sidebar

def main():
    init_session()
    st.set_page_config(layout="wide")
    sidebar.render()

    # Router vers la vue appropriée
    if st.session_state.etape == 1:
        datas_view.render()
    elif st.session_state.etape == 2:
        groups_view.render()
    elif st.session_state.etape == 3:
        menus_view.render()

if __name__ == "__main__":
    main()