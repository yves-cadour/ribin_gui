"""La vue des données"""

import pandas as pd
import plotly.express as px
import streamlit as st
from ..controllers.main_controller import MainController
from ..utils import get_icon, get_label

def render():
    """
    Point d'entrée pour la vue des données
    """
    etape = MainController.get_etape()
    nb_etapes = MainController.get_nb_etapes()
    moulinette = MainController.get_moulinette()
    label, icon = get_label(etape), get_icon(etape)
    st.title(f"{icon} {label} ({etape}/{nb_etapes})")

    if moulinette:
        tab1, tab2 = st.tabs(["📊 Visualisation", "📈 Statistiques"])
        _display_data_tab(tab1)
        _display_stats_tab(tab2)
    else:
        st.info("Veuillez importer un fichier CSV depuis la sidebar")

def _display_data_tab(tab):
    # Implémentation de l'affichage des données...
    moulinette = MainController.get_moulinette()
    with tab:
        st.subheader("Données importées")
        specialites = moulinette.specialites
        # Créer un DataFrame à partir des données de la moulinette
        data = []
        for eleve in moulinette.eleves:
            row = {
                'Nom': eleve.nom,
                'Prénom': eleve.prenom,
                'Classe': eleve.classe
            }
            specialites_eleve = moulinette.get_specialites_for_eleve(eleve)
            for s in specialites:
                row[s.label] = '✓' if s in specialites_eleve else ''
            data.append(row)

        df = pd.DataFrame(data)

        # Réorganiser les colonnes (Nom, Prénom, Classe puis les spécialités)
        cols_order = ['Nom', 'Prénom', 'Classe'] + sorted([s.label for s in specialites])
        df = df[cols_order]

        # Afficher le DataFrame avec style
        st.dataframe(
            df.style.map(
                lambda x: 'color: green; font-weight: bold' if x == '✓' else '',
                subset=[s.label for s in specialites]
            ),
            height=600,
            use_container_width=True,
            hide_index = True,
        )


def _display_stats_tab(tab):
    moulinette = MainController.get_moulinette()
    with tab:
        st.subheader("Statistiques")
        specialites = moulinette.specialites
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
            combinaisons = moulinette.get_eleves_par_combinaison_specialites()

            # Préparation des données
            data = []
            for spes, eleves in combinaisons.items():
                label = " + ".join([f"{s.label}" for s in sorted(spes, key=lambda x: x.label)])
                data.append({'Combinaison': label, 'Effectif': len(eleves)})

            df = pd.DataFrame(data).sort_values('Effectif', ascending=False)

            # Pagination
            items_per_page = 5
            page = st.number_input('Page',
                                   min_value=1,
                                   max_value=len(df)//items_per_page+1,
                                   value=1)

            start_idx = (page-1)*items_per_page
            end_idx = start_idx + items_per_page
            df_page = df.iloc[start_idx:end_idx]

            # Graphique
            fig = px.bar(
                df_page,
                y='Effectif',
                x='Combinaison',
                title=f"Combinaisons de spécialités par popularité \
                    {start_idx+1}-{min(end_idx,len(df))}/{len(df)}",
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
