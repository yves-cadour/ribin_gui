"""Le point d'entrée de l'application"""


from ribin_gui.state import init_state
from ribin_gui.views import main_view

def main():
    """Le point d'entrée de l'application"""
    init_state()
    main_view.render()

if __name__ == "__main__":
    main()
