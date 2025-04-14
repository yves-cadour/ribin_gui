import streamlit as st
from ribin_gui.config.state import init_state
from ribin_gui.components.sidebar import sidebar
from ribin_gui.views import import_view, groups_view, menus_view


def main():
    init_state()
    sidebar()

    if st.session_state.etape == 1:
        import_view.render()
    elif st.session_state.etape == 2:
        groups_view.render()
    elif st.session_state.etape == 3:
        menus_view.render()

if __name__ == "__main__":
    main()