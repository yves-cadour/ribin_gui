"""Une GUI streamlit"""

import streamlit as st
import pandas as pd
import plotly.express as px
from ribin.moulinette import Moulinette
from ribin_gui.utils import calculer_separateurs

# Configuration de la page
def config_page():
    st.set_page_config(layout="wide", page_title="Gestion des menus de spécialités")
    st.markdown("""
    <style>
        .sidebar .stButton>button { width: 100%; margin: 5px 0; }
        div[data-testid="stExpander"] div[role="button"] p { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Initialisation de l'état
def init_state():
    if 'etape' not in st.session_state:
        st.session_state.etape = 1  # 1=Import, 2=Groupes, 3=Menus
    if 'moulinette' not in st.session_state:
        st.session_state.moulinette = None

# Fonctions pour gérer les groupes
def ajouter_groupe_ui(spe_label: str):
    spe = next(s for s in st.session_state.moulinette.specialites if s.label == spe_label)
    g = spe.ajouter_groupe()
    reset_menus(origine="ajouter_groupe_ui")
    st.session_state.success_message = f"Nouveau groupe {g.id} créé"
    st.rerun()

def reset_menus(origine = ""):
    debug = False
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

# Affichage en vrac


# Étape 1 - Import des données
def etape_import():
    st.title("📤 Importation des données")

    if st.session_state.moulinette:
        tab1, tab2 = st.tabs(["📊 Visualisation", "📈 Statistiques"])

        with tab1:
            st.subheader("Données importées")

            # Créer un DataFrame à partir des données de la moulinette
            data = []
            for eleve in st.session_state.moulinette.eleves:
                row = {
                    'Nom': eleve.nom,
                    'Prénom': eleve.prenom,
                    'Classe': eleve.classe
                }
                specialites = st.session_state.moulinette.get_specialites_for_eleve(eleve)
                for s in st.session_state.moulinette.specialites:
                    row[s.label] = '✓' if s in specialites else ''
                data.append(row)

            df = pd.DataFrame(data)

            # Réorganiser les colonnes (Nom, Prénom, Classe puis les spécialités)
            cols_order = ['Nom', 'Prénom', 'Classe'] + sorted([s.label for s in st.session_state.moulinette.specialites])
            df = df[cols_order]

            # Afficher le DataFrame avec style
            st.dataframe(
                df.style.applymap(
                    lambda x: 'color: green; font-weight: bold' if x == '✓' else '',
                    subset=[s.label for s in st.session_state.moulinette.specialites]
                ),
                height=600,
                use_container_width=True,
                hide_index = True,
            )

        with tab2:
            st.subheader("Statistiques")
            specialites = st.session_state.moulinette.specialites
            col1, col2 = st.columns(2)
            with col1:
                # Création d'un DataFrame
                df = pd.DataFrame({
                    'Spécialité': [f"{s.icon} {s.label}" for s in specialites],
                    'Effectif': [len(s.default_groupe.eleves) for s in specialites]
                })
                df = df.sort_values('Effectif', ascending=False)

               # Création du graphique
                fig = px.bar(
                    df,
                    x='Spécialité',
                    y='Effectif',
                    title="Effectifs par spécialité",
                    text='Effectif',
                )

                # Personnalisation
                fig.update_traces(textposition='outside')
                fig.update_layout(showlegend=False)
                # Affichage dans Streamlit
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                combinaisons = st.session_state.moulinette.get_eleves_par_combinaison_specialites()

                # Préparation des données
                data = []
                for spes, eleves in combinaisons.items():
                    label = " + ".join([f"{s.label}" for s in sorted(spes, key=lambda x: x.label)])
                    data.append({'Combinaison': label, 'Effectif': len(eleves)})

                df = pd.DataFrame(data).sort_values('Effectif', ascending=False)

                # Pagination
                items_per_page = 5
                page = st.number_input('Page', min_value=1, max_value=len(df)//items_per_page+1, value=1)

                start_idx = (page-1)*items_per_page
                end_idx = start_idx + items_per_page
                df_page = df.iloc[start_idx:end_idx]

                # Graphique
                fig = px.bar(
                    df_page,
                    y='Effectif',
                    x='Combinaison',
                    title=f"Combinaisons de spécialités par popularité {start_idx+1}-{min(end_idx,len(df))}/{len(df)}",
                    text='Effectif',
                )

                fig.update_layout(
                    yaxis={'categoryorder':'total ascending'},
                    height=400,
                    xaxis_title="Combinaison de spécialités",
                    yaxis_title="Nombre d'élèves"
                )

                #fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)



    else:
        st.info("Veuillez importer un fichier CSV depuis la sidebar")

# Étape 2 - Gestion des groupes
def etape_groupes():
    st.title("👥 Gestion des groupes")

    if not st.session_state.moulinette:
        st.warning("Importez d'abord un fichier valide")
        return

    specialites = st.session_state.moulinette.specialites
    separateurs = calculer_separateurs(len(specialites), 3)
    cols = st.columns(len(separateurs))

    for col, (start, end) in zip(cols, separateurs):
        with col:
            for spe in specialites[start:end]:
                with st.expander(f"{spe.icon}{spe.label} ({len(spe.eleves)} élèves)", expanded=True):
                    # Bouton Ajouter
                    if st.button("➕ Ajouter un groupe", key=f"add_{spe.label}"):
                        st.session_state.moulinette.add_groupe(spe)
                    # Liste des groupes existants
                    if spe.groupes:
                        for groupe in sorted(spe.groupes, key=lambda x: x.number):
                            cols = st.columns([4, 1])
                            cols[0].write(f"Groupe {groupe.label}: {len(groupe.eleves)} élèves")
                            if groupe.number != 1 and cols[1].button("➖", key=f"del_{groupe.id}"):
                                st.session_state.moulinette.delete_groupe(groupe.id)
                    else:
                        st.warning("Aucun groupe créé")

# Étape 3 - Génération des menus
def etape_menus():
    st.title("Génération des menus")
    moulinette = st.session_state.moulinette

    if not moulinette:
        st.warning("Complétez les étapes précédentes")
        return

    if 'menus' not in st.session_state:
        st.session_state.menus = None
    if 'current_menu_index' not in st.session_state:
        st.session_state.current_menu_index = 0

    if st.session_state.menus:
        menus = st.session_state.menus
        total_menus = len(menus)
        menu_index = st.session_state.current_menu_index

        # Conteneur de navigation
        nav_container = st.container()
        with nav_container:
            cols_nav = st.columns([1, 2, 1])
            with cols_nav[0]:
                if st.button("← Précédent",
                           disabled=menu_index == 0,
                           type="primary"):
                    st.session_state.current_menu_index -= 1
                    st.rerun()
            with cols_nav[1]:
                st.subheader(f"Menu {menu_index + 1}/{total_menus}")
            with cols_nav[2]:
                if st.button("Suivant →",
                           disabled=menu_index >= total_menus - 1,
                           type="primary"):
                    st.session_state.current_menu_index += 1
                    st.rerun()

        # Affichage des barrettes
        current_menu = menus[menu_index]
        barrettes = current_menu.barrettes  # C'est un FrozenSet[Barrette]

        # Créer des colonnes pour afficher les barrettes
        cols = st.columns(len(barrettes), gap="small")

        for i, (col, barrette) in enumerate(zip(cols, barrettes)):
            with col:
                st.markdown(f"**☰&nbsp;&nbsp;BARRETTE {i+1}**")
                # Afficher les groupes de la barrette
                for groupe in barrette.groupes:  # Utilisez la propriété groupes
                    spe = groupe.specialite
                    st.markdown(f"""
                    <div style="border-top:1px solid #ccc;padding:5px 0">
                        <b>{spe.icon} {groupe.label}</b><small>&nbsp;{len(groupe.eleves)} élèves</small>
                    </div>
                    """, unsafe_allow_html=True)

        # Affichage des conflits
        certains, potentiels = current_menu.conflicts(moulinette)
        st.subheader("Conflits par concomitance")
        cols = st.columns(len((certains, potentiels)), gap="small")
        for i, (col, eleves) in enumerate(zip(cols, (certains, potentiels))):
            with col:
                with st.expander(f"Conflits {"certains" if i==0 else "potentiels" } ({len(eleves)} élèves)", expanded=True):
                    if eleves:
                        st.dataframe(pd.DataFrame(
                            [(f"{e.nom} {e.prenom}", ", ".join(s.label for s in moulinette.get_specialites_for_eleve(e)))
                            for e in sorted(eleves, key=lambda x: moulinette.get_specialites_for_eleve(x))],
                            columns=["Élève", "Spécialités"]
                        ), hide_index=True)
                        # for eleve in certains:
                        #     conflits_eleve = st.session_state.moulinette.get_conflicts_for_eleve_in_menu(eleve, st.session_state.menus[0])
                        #     for barrette, groupes in conflits_eleve:
                        #         st.markdown(f"**Conflits dans la barrette {barrette.label}**")
                        #         for groupe in groupes:
                        #             st.markdown(f"- {groupe.specialite.label} ({groupe.label})")
                    else:
                        st.info("Aucun conflit")

    elif 'menus' in st.session_state and st.session_state.menus is None:
        st.info("Générez les menus en cliquant sur le bouton dans la partie gauche.")

# Barre latérale de navigation
def sidebar_navigation():
    with st.sidebar:
        # Navigation entre étapes
        st.title("Navigation")
        col1, col2 = st.columns(2)
        texte_retour = "← Retour"
        texte_suivant = "Suivant →"
        if st.session_state.etape > 1:
            if col1.button(texte_retour):
                st.session_state.etape -= 1
                st.rerun()
        if st.session_state.moulinette and st.session_state.etape < 3:
            if col2.button(texte_suivant):
                st.session_state.etape += 1
                st.rerun()

        # Étape 1 - Import
        if st.session_state.etape == 1:
            st.header("1. Données")
            uploaded_file = st.file_uploader("Importer CSV", type=["csv"])
            if uploaded_file and not st.session_state.moulinette:
                st.session_state.moulinette = Moulinette()
                # 1. Lire le CSV directement avec pandas
                df = pd.read_csv(uploaded_file)
                # Convertir le fichier uploadé en bytes avant de le passer à read_datas
                st.session_state.moulinette.read_datas(df)
                reset_menus(origine="upload csv")
                st.success("Fichier importé !")
                st.rerun()

        # Étape 3 - Menus
        if st.session_state.etape == 3:
            st.header("3. Détermination du nombre de barrettes")
            nb_barrettes = st.slider("Nombre de barrettes",
                                     min_value=2,
                                     max_value=5,
                                     value=st.session_state.moulinette.nb_barrettes,
                                     on_change=reset_menus)
            if st.session_state.moulinette:
                st.session_state.moulinette.nb_barrettes = nb_barrettes
                # Réinitialiser les conflits quand on change le nombre de barrettes
                #st.session_state.menus = None

            if st.button("🎯 Générer les menus", type="primary"):
                with st.spinner("Génération en cours..."):
                    st.session_state.menus = st.session_state.moulinette.menus_tries_par_conflits_et_filtres(max_par_conflit_certain=5)
#                    st.session_state.menus = st.session_state.moulinette.menus_tries_par_conflits()
                    st.session_state.current_menu_index = 0
                    st.rerun()

# Fonction principale
def main():
    """Fonction principale de l'application Streamlit"""
    config_page()
    init_state()
    sidebar_navigation()

    # Gestion des messages
    if 'success_message' in st.session_state:
        st.success(st.session_state.pop('success_message'))
    if 'error_message' in st.session_state:
        st.error(st.session_state.pop('error_message'))

    # Affichage de l'étape courante
    if st.session_state.etape == 1:
        etape_import()
    elif st.session_state.etape == 2:
        etape_groupes()
    elif st.session_state.etape == 3:
        etape_menus()

if __name__ == "__main__":
    main()

